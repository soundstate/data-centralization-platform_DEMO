# 🎨 Figma AI Design Prompt - Intelligent Document Management Chatbot

## **Core Design Brief**

Create a modern, elegant chatbot interface for an enterprise document management system that uses AI to intelligently organize and store business documents. The interface should feel professional yet approachable, suitable for business users across legal, insurance, healthcare, and corporate environments.

---

## **Primary Interface Requirements**

### **Chat Interface Design**
- **Clean, modern chat layout** similar to ChatGPT or Claude, but with enterprise styling
- **Professional color scheme** using blues, grays, and whites (avoid bright consumer colors)
- **Message bubbles** with clear distinction between user messages and AI assistant responses
- **Typography** should be highly readable and business-appropriate (think Slack or Microsoft Teams aesthetic)
- **Generous white space** for a clean, uncluttered feel

### **Document Upload Zone**
- **Drag-and-drop file upload area** integrated seamlessly into the chat interface
- **Multiple file upload support** with visual indicators for each file
- **File preview thumbnails** showing document icons and filenames
- **Upload progress indicators** with percentage completion
- **File type icons** (PDF, DOCX, XLSX, etc.) with clear visual hierarchy

### **AI Suggestion Display**
- **Structured suggestion cards** that show:
  - Proposed file path with folder hierarchy visualization
  - Suggested filename with highlighted components
  - Confidence score indicator (progress bar or percentage)
  - Reasoning explanation in readable format
- **Action buttons** for "Approve", "Modify", or "Reject" suggestions
- **Collapsible sections** for detailed analysis and metadata

---

## **Specific UI Components Needed**

### **1. Chat Message Types**
```
USER MESSAGE EXAMPLE:
"I need to file this marketing contract with ABC Corp for our Q1 campaign"
[Attached: Marketing_Contract_Draft.pdf]

AI RESPONSE EXAMPLE:
Card showing:
📁 Suggested Location: /Legal/Contracts/2025/Q1/Marketing/ABC_Corp/
📄 Filename: 2025-01-20_Marketing-Contract_ABC-Corp_Q1-Campaign_DRAFT.pdf
🎯 Confidence: 92%
💭 Reasoning: "Based on document content analysis, I identified this as a marketing contract with ABC Corp for Q1 2025..."
[Approve] [Modify] [Reject]
```

### **2. Multi-Document Organization View**
- **Folder tree visualization** showing proposed document organization
- **Batch approval interface** with "Approve All" and "Review Individual" options
- **Document list** with thumbnail previews and proposed locations
- **Status indicators** (Pending, Approved, Filed, Error)

### **3. File Management Components**
- **File upload progress bars** with file names and sizes
- **Error state indicators** for upload failures or processing issues
- **Success confirmations** when documents are successfully filed
- **Metadata display cards** showing extracted information

### **4. Navigation and Controls**
- **Sidebar with recent conversations** (collapsible)
- **Settings/preferences panel** for user configurations
- **Help/tutorial overlay** for first-time users
- **User profile dropdown** with role and permissions

---

## **Visual Design Guidelines**

### **Color Palette**
- **Primary Blue**: #2563eb (professional, trustworthy)
- **Secondary Gray**: #64748b (neutral, readable)
- **Background**: #f8fafc (clean, modern)
- **Success Green**: #10b981 (confirmations)
- **Warning Orange**: #f59e0b (attention needed)
- **Error Red**: #ef4444 (problems)
- **White**: #ffffff (cards, containers)

### **Typography Hierarchy**
- **Headings**: Inter or Roboto, medium weight
- **Body text**: Inter or Roboto, regular weight
- **Code/filenames**: Monaco or Consolas, monospace
- **Buttons**: Inter, medium weight

### **Component Styling**
- **Rounded corners**: 8px for cards, 6px for buttons
- **Drop shadows**: Subtle, professional (not heavy consumer-style)
- **Border radius**: Consistent across all components
- **Spacing**: 16px, 24px, 32px grid system
- **Icon style**: Outline or minimal filled icons (Heroicons style)

---

## **User Experience Flow Mockups**

### **Screen 1: Empty State / Welcome**
- **Clean welcome message** explaining the system
- **Sample prompts** users can click to get started
- **Upload zone** prominently displayed but not overwhelming
- **Brief tutorial** or "How it works" section

### **Screen 2: Active Chat with Document Upload**
- **Chat history** showing conversation context
- **File upload area** with drag-and-drop active state
- **Processing indicators** while AI analyzes documents
- **Real-time typing indicators** for AI responses

### **Screen 3: AI Suggestions Display**
- **Detailed suggestion cards** with all proposed information
- **Visual file path** showing folder structure
- **Confidence indicators** and reasoning
- **Clear action buttons** for user decisions

### **Screen 4: Multi-Document Organization**
- **Tree view** of proposed folder structure
- **Document list** with status indicators
- **Batch actions** prominently displayed
- **Progress tracking** for filing operations

### **Screen 5: Success/Completion State**
- **Confirmation messages** with links to filed documents
- **Summary of actions taken**
- **Suggestions for next steps** or related actions

---

## **Mobile Responsive Considerations**
- **Collapsible sidebar** that slides out on mobile
- **Stacked suggestion cards** instead of side-by-side layout
- **Touch-friendly buttons** with adequate spacing
- **Simplified file upload** with mobile-optimized interface
- **Readable text sizes** on small screens

---

## **Accessibility Requirements**
- **High contrast ratios** meeting WCAG 2.1 AA standards
- **Keyboard navigation** support for all interactive elements
- **Screen reader friendly** with proper ARIA labels
- **Focus indicators** clearly visible for keyboard users
- **Alternative text** for all icons and images

---

## **Enterprise Features to Include**

### **Status and Progress Indicators**
- **Processing status badges** (Analyzing, Filing, Complete, Error)
- **Progress bars** for upload and processing operations
- **Queue indicators** showing pending documents
- **System health indicators** (optional, in settings)

### **User Context Elements**
- **User role badge** (Analyst, Admin, Viewer)
- **Organization branding** area (logo, colors)
- **Permission indicators** showing what user can access
- **Audit trail breadcrumbs** for compliance

### **Advanced Controls**
- **Filter and search** within chat history
- **Bookmark/favorite** frequently used paths
- **Settings panel** for preferences and configurations
- **Help and support** integration

---

## **Technical Implementation Hints**

### **Component Architecture**
- **Modular design system** with reusable components
- **Consistent spacing and sizing** across all elements
- **Scalable icon system** with multiple sizes
- **Theme support** for light/dark modes (start with light)

### **Animation and Interactions**
- **Smooth transitions** between states (300ms duration)
- **Hover effects** for interactive elements
- **Loading animations** for processing states
- **Micro-interactions** for user feedback
- **Page transitions** that feel natural and professional

---

## **Inspiration References**
- **Slack** for overall chat interface feel
- **Linear** for clean, modern enterprise design
- **Notion** for card-based information display
- **GitHub** for file management and organization
- **Figma** itself for professional tool aesthetics

---

## **Final Design Deliverables Requested**

1. **Desktop Layout** (1440px width)
   - Empty state welcome screen
   - Active chat with file upload
   - AI suggestions display
   - Multi-document organization view

2. **Mobile Layout** (375px width)
   - Responsive versions of key screens
   - Mobile-optimized interactions

3. **Component Library**
   - Chat bubbles and message types
   - File upload components
   - Suggestion cards and approval buttons
   - Navigation and control elements

4. **Design System Documentation**
   - Color palette with usage guidelines
   - Typography scale and hierarchy
   - Spacing and layout grid
   - Icon library and usage rules

**Style Direction**: Professional, clean, modern enterprise software that feels approachable and intelligent. Think "if Slack and ChatGPT had a business-focused child designed for document management."
