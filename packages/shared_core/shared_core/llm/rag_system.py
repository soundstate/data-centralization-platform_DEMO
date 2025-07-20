"""
RAG (Retrieval-Augmented Generation) System

Enables natural language querying of cross-domain correlations and insights
using semantic search and LLM generation.
"""

import asyncio
import os
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import json

from openai import AsyncOpenAI
import pandas as pd
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from ..embeddings.embedding_service import EmbeddingService
from ..database.connection.database_manager import DatabaseManager
from ..database.models import Correlation, TimeSeriesData


@dataclass
class RAGResponse:
    """Response from the RAG system"""
    query: str
    answer: str
    source_correlations: List[Dict[str, Any]]
    source_entities: List[Dict[str, Any]]
    confidence: float
    metadata: Dict[str, Any]


@dataclass
class CorrelationContext:
    """Context about correlations for LLM generation"""
    correlations: List[Dict[str, Any]]
    statistical_summary: Dict[str, Any]
    business_insights: List[str]
    entity_links: List[Dict[str, Any]]


class CorrelationRAGSystem:
    """
    Retrieval-Augmented Generation system for correlation analysis queries
    """
    
    def __init__(self, 
                 model_name: str = "gpt-4o-mini",
                 api_key: Optional[str] = None):
        """
        Initialize the RAG system
        
        Args:
            model_name: OpenAI model for text generation
            api_key: OpenAI API key (defaults to environment variable)
        """
        self.model_name = model_name
        
        # Initialize services
        api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable.")
        
        self.llm_client = AsyncOpenAI(api_key=api_key)
        self.embedding_service = EmbeddingService(api_key=api_key)
        self.db_manager = DatabaseManager()
        
        # System prompts for different query types
        self.system_prompts = {
            "correlation": """You are a data analyst expert specializing in cross-domain correlation analysis. 
            You help users understand relationships between different types of data (music, weather, entertainment, gaming, etc.).
            
            Provide clear, actionable insights based on the correlation data provided. Focus on:
            1. Statistical significance and strength of correlations
            2. Business implications and practical applications
            3. Potential causation vs correlation distinctions
            4. Recommendations for further analysis or action
            
            Be precise about statistical measures and avoid overstating conclusions.""",
            
            "search": """You are a semantic search assistant for a multi-domain data platform.
            Help users find relevant entities and content across music, entertainment, weather, gaming, development, and productivity domains.
            
            Provide context about search results and suggest related queries or entities that might be of interest.
            Focus on connecting related concepts across different domains.""",
            
            "insights": """You are a business intelligence analyst helping users discover actionable insights 
            from cross-domain data correlations. 
            
            Generate specific, practical recommendations based on the correlation patterns and entity relationships provided.
            Consider seasonal patterns, geographic factors, and demographic implications in your analysis."""
        }
    
    async def query_correlations(self, 
                               query: str,
                               query_type: str = "correlation",
                               k: int = 5) -> RAGResponse:
        """
        Answer natural language questions about data correlations
        
        Args:
            query: User's natural language query
            query_type: Type of query (correlation, search, insights)
            k: Number of relevant items to retrieve
            
        Returns:
            RAGResponse with answer and sources
        """
        try:
            # Step 1: Semantic search for relevant entities
            entity_results = await self.embedding_service.semantic_search(
                query, domain=None, k=k
            )
            
            # Step 2: Retrieve relevant correlations from database
            correlation_results = await self._retrieve_relevant_correlations(
                query, entity_results, k=k
            )
            
            # Step 3: Build context for LLM
            context = await self._build_correlation_context(
                correlation_results, entity_results
            )
            
            # Step 4: Generate response using LLM
            answer = await self._generate_llm_response(
                query, context, query_type
            )
            
            # Step 5: Calculate confidence score
            confidence = self._calculate_response_confidence(
                correlation_results, entity_results
            )
            
            return RAGResponse(
                query=query,
                answer=answer,
                source_correlations=correlation_results,
                source_entities=entity_results,
                confidence=confidence,
                metadata={
                    "timestamp": datetime.now().isoformat(),
                    "query_type": query_type,
                    "model_used": self.model_name,
                    "entities_retrieved": len(entity_results),
                    "correlations_retrieved": len(correlation_results)
                }
            )
            
        except Exception as e:
            return RAGResponse(
                query=query,
                answer=f"I apologize, but I encountered an error processing your query: {str(e)}",
                source_correlations=[],
                source_entities=[],
                confidence=0.0,
                metadata={"error": str(e)}
            )
    
    async def _retrieve_relevant_correlations(self, 
                                            query: str,
                                            entity_results: List[Dict[str, Any]],
                                            k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve correlations relevant to the query and entities
        """
        correlations = []
        
        # Extract domains from entity results
        domains = set(result["domain"] for result in entity_results)
        
        async with self.db_manager.async_session() as session:
            try:
                # Query correlations involving the relevant domains
                if domains:
                    domain_list = list(domains)
                    correlation_query = text("""
                        SELECT 
                            domain1, domain2, variable1, variable2,
                            correlation_coefficient, p_value, sample_size,
                            analysis_method, is_significant, significance_level,
                            metadata_json, created_at
                        FROM analytics.correlations
                        WHERE domain1 IN :domains OR domain2 IN :domains
                        ORDER BY ABS(correlation_coefficient) DESC, p_value ASC
                        LIMIT :limit
                    """)
                    
                    result = await session.execute(
                        correlation_query,
                        {"domains": tuple(domain_list), "limit": k * 2}
                    )
                    
                    for row in result:
                        correlations.append({
                            "domain1": row.domain1,
                            "domain2": row.domain2,
                            "variable1": row.variable1,
                            "variable2": row.variable2,
                            "correlation_coefficient": float(row.correlation_coefficient),
                            "p_value": float(row.p_value),
                            "sample_size": row.sample_size,
                            "method": row.analysis_method,
                            "is_significant": row.is_significant,
                            "significance_level": float(row.significance_level),
                            "interpretation": row.metadata_json or {},
                            "created_at": row.created_at.isoformat() if row.created_at else None
                        })
                
                # Also get some general high-significance correlations
                general_query = text("""
                    SELECT 
                        domain1, domain2, variable1, variable2,
                        correlation_coefficient, p_value, sample_size,
                        analysis_method, is_significant, significance_level,
                        metadata_json, created_at
                    FROM analytics.correlations
                    WHERE is_significant = true
                    ORDER BY ABS(correlation_coefficient) DESC, p_value ASC
                    LIMIT :limit
                """)
                
                result = await session.execute(general_query, {"limit": k})
                
                for row in result:
                    corr_dict = {
                        "domain1": row.domain1,
                        "domain2": row.domain2,
                        "variable1": row.variable1,
                        "variable2": row.variable2,
                        "correlation_coefficient": float(row.correlation_coefficient),
                        "p_value": float(row.p_value),
                        "sample_size": row.sample_size,
                        "method": row.analysis_method,
                        "is_significant": row.is_significant,
                        "significance_level": float(row.significance_level),
                        "interpretation": row.metadata_json or {},
                        "created_at": row.created_at.isoformat() if row.created_at else None
                    }
                    
                    # Avoid duplicates
                    if corr_dict not in correlations:
                        correlations.append(corr_dict)
            
            except Exception as e:
                print(f"Error retrieving correlations: {e}")
        
        return correlations[:k]
    
    async def _build_correlation_context(self, 
                                       correlations: List[Dict[str, Any]],
                                       entities: List[Dict[str, Any]]) -> CorrelationContext:
        """
        Build comprehensive context for LLM generation
        """
        # Statistical summary
        if correlations:
            corr_coefficients = [abs(c["correlation_coefficient"]) for c in correlations]
            p_values = [c["p_value"] for c in correlations]
            significant_count = sum(1 for c in correlations if c["is_significant"])
            
            statistical_summary = {
                "total_correlations": len(correlations),
                "significant_correlations": significant_count,
                "avg_correlation_strength": sum(corr_coefficients) / len(corr_coefficients),
                "min_p_value": min(p_values) if p_values else 1.0,
                "max_correlation": max(corr_coefficients) if corr_coefficients else 0.0,
                "domains_involved": list(set([c["domain1"] for c in correlations] + [c["domain2"] for c in correlations]))
            }
        else:
            statistical_summary = {
                "total_correlations": 0,
                "significant_correlations": 0,
                "avg_correlation_strength": 0.0,
                "min_p_value": 1.0,
                "max_correlation": 0.0,
                "domains_involved": []
            }
        
        # Generate business insights
        business_insights = self._generate_business_insights(correlations)
        
        # Entity links (from semantic search)
        entity_links = [
            {
                "content": entity["content"],
                "entity_type": entity["entity_type"],
                "domain": entity["domain"],
                "similarity": entity["similarity"]
            }
            for entity in entities
        ]
        
        return CorrelationContext(
            correlations=correlations,
            statistical_summary=statistical_summary,
            business_insights=business_insights,
            entity_links=entity_links
        )
    
    def _generate_business_insights(self, correlations: List[Dict[str, Any]]) -> List[str]:
        """Generate business insights from correlation patterns"""
        insights = []
        
        for corr in correlations:
            if not corr["is_significant"]:
                continue
                
            strength = abs(corr["correlation_coefficient"])
            domain1 = corr["domain1"]
            domain2 = corr["domain2"]
            
            if strength >= 0.7:
                insights.append(
                    f"Strong correlation detected between {domain1} and {domain2} "
                    f"({corr['variable1']} ↔ {corr['variable2']}). "
                    f"This suggests potential for integrated marketing or predictive modeling."
                )
            elif strength >= 0.5:
                insights.append(
                    f"Moderate correlation found between {domain1} and {domain2}. "
                    f"Consider investigating causal relationships or common factors."
                )
            
            # Domain-specific insights
            if {domain1, domain2} == {"weather", "music"}:
                insights.append(
                    "Weather-music correlations suggest opportunities for mood-based "
                    "playlist recommendations or seasonal marketing campaigns."
                )
            elif {domain1, domain2} == {"entertainment", "music"}:
                insights.append(
                    "Entertainment-music correlations indicate potential for "
                    "synchronized release strategies or cross-promotional opportunities."
                )
        
        return list(set(insights))  # Remove duplicates
    
    async def _generate_llm_response(self, 
                                   query: str,
                                   context: CorrelationContext,
                                   query_type: str) -> str:
        """
        Generate LLM response using retrieved context
        """
        # Build context string for the LLM
        context_str = self._format_context_for_llm(context)
        
        system_prompt = self.system_prompts.get(query_type, self.system_prompts["correlation"])
        
        try:
            response = await self.llm_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user", 
                        "content": f"""Based on the following data context, please answer this question: {query}
                        
Context:
{context_str}

Please provide a comprehensive answer that:
1. Addresses the specific question asked
2. References relevant correlations and their statistical significance
3. Provides actionable insights or recommendations
4. Distinguishes between correlation and potential causation
5. Suggests areas for further investigation if relevant"""
                    }
                ],
                temperature=0.3,  # Lower temperature for more consistent analytical responses
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"I apologize, but I encountered an error generating the response: {str(e)}"
    
    def _format_context_for_llm(self, context: CorrelationContext) -> str:
        """Format context information for LLM consumption"""
        
        context_parts = []
        
        # Statistical Summary
        summary = context.statistical_summary
        context_parts.append(f"""
Statistical Summary:
- Total correlations analyzed: {summary['total_correlations']}
- Statistically significant: {summary['significant_correlations']}
- Average correlation strength: {summary['avg_correlation_strength']:.3f}
- Strongest correlation: {summary['max_correlation']:.3f}
- Domains involved: {', '.join(summary['domains_involved'])}
""")
        
        # Significant Correlations
        if context.correlations:
            context_parts.append("\\nKey Correlations:")
            for i, corr in enumerate(context.correlations[:5], 1):  # Top 5 correlations
                significance = "significant" if corr["is_significant"] else "not significant"
                context_parts.append(
                    f"{i}. {corr['domain1']} ↔ {corr['domain2']}: "
                    f"{corr['variable1']} vs {corr['variable2']} "
                    f"(r={corr['correlation_coefficient']:.3f}, p={corr['p_value']:.3f}, {significance})"
                )
        
        # Business Insights
        if context.business_insights:
            context_parts.append("\\nBusiness Insights:")
            for insight in context.business_insights:
                context_parts.append(f"- {insight}")
        
        # Relevant Entities
        if context.entity_links:
            context_parts.append("\\nRelevant Entities:")
            for entity in context.entity_links[:3]:  # Top 3 entities
                context_parts.append(
                    f"- [{entity['entity_type']}] {entity['content']} "
                    f"(Domain: {entity['domain']}, Similarity: {entity['similarity']:.3f})"
                )
        
        return "\\n".join(context_parts)
    
    def _calculate_response_confidence(self, 
                                     correlations: List[Dict[str, Any]],
                                     entities: List[Dict[str, Any]]) -> float:
        """
        Calculate confidence score for the response
        
        Factors:
        - Number of significant correlations found
        - Strength of correlations
        - Quality of entity matches
        - Statistical significance levels
        """
        if not correlations and not entities:
            return 0.0
        
        confidence_factors = []
        
        # Correlation factors
        if correlations:
            significant_ratio = sum(1 for c in correlations if c["is_significant"]) / len(correlations)
            avg_strength = sum(abs(c["correlation_coefficient"]) for c in correlations) / len(correlations)
            min_p_value = min(c["p_value"] for c in correlations)
            
            confidence_factors.extend([
                significant_ratio * 0.4,  # 40% weight for significance
                avg_strength * 0.3,       # 30% weight for strength
                (1 - min_p_value) * 0.2   # 20% weight for p-value quality
            ])
        
        # Entity similarity factors
        if entities:
            avg_similarity = sum(1 - e["similarity"] for e in entities) / len(entities)  # Convert distance to similarity
            confidence_factors.append(avg_similarity * 0.1)  # 10% weight
        
        # Overall confidence (capped at 0.95 to indicate some uncertainty)
        confidence = min(sum(confidence_factors), 0.95)
        return max(confidence, 0.1)  # Minimum confidence of 0.1
    
    async def suggest_related_queries(self, original_query: str, k: int = 3) -> List[str]:
        """
        Suggest related queries based on the original query
        """
        try:
            response = await self.llm_client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a query suggestion assistant for a multi-domain data analysis platform. "
                                 "Generate related questions that users might want to ask based on their original query. "
                                 "Focus on cross-domain relationships, seasonal patterns, geographic factors, and business implications."
                    },
                    {
                        "role": "user",
                        "content": f"Based on this query: '{original_query}', suggest {k} related questions "
                                 f"about data correlations across domains (music, weather, entertainment, gaming, development, productivity). "
                                 f"Return only the questions, one per line."
                    }
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            suggestions = response.choices[0].message.content.strip().split('\\n')
            return [s.strip().strip('-').strip() for s in suggestions if s.strip()][:k]
            
        except Exception as e:
            print(f"Error generating query suggestions: {e}")
            return []


# Demo and utility functions
async def demo_rag_queries():
    """
    Demonstrate RAG system with sample queries
    """
    rag_system = CorrelationRAGSystem()
    
    sample_queries = [
        "What correlations exist between weather and music preferences?",
        "How does movie box office performance relate to soundtrack success?",
        "Are there seasonal patterns in gaming activity and entertainment consumption?",
        "What programming languages correlate with project success metrics?",
        "How do weather patterns affect productivity and work habits?"
    ]
    
    print("🤖 RAG System Demo - Natural Language Data Queries")
    print("=" * 60)
    
    for i, query in enumerate(sample_queries, 1):
        print(f"\\n{i}. Query: {query}")
        print("-" * 40)
        
        try:
            response = await rag_system.query_correlations(query)
            
            print(f"Answer: {response.answer}")
            print(f"\\nConfidence: {response.confidence:.2f}")
            print(f"Sources: {len(response.source_correlations)} correlations, {len(response.source_entities)} entities")
            
            if response.source_correlations:
                print("\\nTop Correlations Referenced:")
                for corr in response.source_correlations[:2]:
                    print(f"  • {corr['domain1']} ↔ {corr['domain2']}: r={corr['correlation_coefficient']:.3f}")
            
            # Suggest related queries
            suggestions = await rag_system.suggest_related_queries(query)
            if suggestions:
                print("\\nRelated Questions:")
                for suggestion in suggestions:
                    print(f"  ? {suggestion}")
            
            print("\\n" + "="*60)
            
        except Exception as e:
            print(f"Error processing query: {e}")
            continue
        
        # Small delay between queries
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(demo_rag_queries())
