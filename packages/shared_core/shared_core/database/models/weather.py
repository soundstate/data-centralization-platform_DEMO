"""
Weather Domain Models

SQLAlchemy models for weather data from OpenWeatherMap API.
Includes geographic coordinates for location-based correlation analysis.
"""

from typing import Optional, Dict, Any
from decimal import Decimal
from sqlalchemy import String, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin


class Location(BaseModel, EmbeddingMixin, CorrelationMixin, TimestampMixin):
    """
    Location model for weather data with geographic correlation support
    """
    __tablename__ = 'locations'
    __table_args__ = {'schema': 'weather'}
    
    # Location identification
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    country: Mapped[Optional[str]] = mapped_column(String(100))
    state: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Geographic coordinates - critical for location-based correlations
    latitude: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(10, 8), 
        index=True,
        comment="Latitude for geographic correlation analysis"
    )
    longitude: Mapped[Optional[Decimal]] = mapped_column(
        Numeric(11, 8), 
        index=True,
        comment="Longitude for geographic correlation analysis"
    )
    
    # Timezone for temporal correlation
    timezone: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Additional location data
    population: Mapped[Optional[int]] = mapped_column(Integer)
    elevation: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Relationships
    current_weather: Mapped[list["CurrentWeather"]] = relationship(
        "CurrentWeather", 
        back_populates="location"
    )
    historical_weather: Mapped[list["HistoricalWeather"]] = relationship(
        "HistoricalWeather", 
        back_populates="location"
    )
    
    def get_coordinate_tuple(self) -> tuple:
        """Get coordinates as tuple for distance calculations"""
        if self.latitude and self.longitude:
            return (float(self.latitude), float(self.longitude))
        return None
    
    def __repr__(self):
        return f"<Location(name='{self.name}', lat={self.latitude}, lon={self.longitude})>"


class CurrentWeather(BaseModel, CorrelationMixin, TimestampMixin):
    """
    Current weather conditions with mood and behavioral correlation potential
    """
    __tablename__ = 'current_weather'
    __table_args__ = {'schema': 'weather'}
    
    # Location reference
    location_id: Mapped[str] = mapped_column(ForeignKey('weather.locations.id'))
    
    # Temperature data - key for behavioral correlations
    temperature: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))  # Celsius
    feels_like: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    temperature_min: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    temperature_max: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    
    # Atmospheric conditions
    humidity: Mapped[Optional[int]] = mapped_column(Integer)  # Percentage
    pressure: Mapped[Optional[int]] = mapped_column(Integer)  # hPa
    visibility: Mapped[Optional[int]] = mapped_column(Integer)  # meters
    
    # UV and light conditions - affects mood/behavior
    uv_index: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 1))
    
    # Wind conditions
    wind_speed: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))  # m/s
    wind_direction: Mapped[Optional[int]] = mapped_column(Integer)  # degrees
    wind_gust: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))  # m/s
    
    # Weather description
    weather_condition: Mapped[Optional[str]] = mapped_column(
        String(100),
        index=True,
        comment="Main weather condition - key for behavioral correlation"
    )
    description: Mapped[Optional[str]] = mapped_column(String)
    icon: Mapped[Optional[str]] = mapped_column(String(10))
    
    # Cloud and precipitation
    cloud_cover: Mapped[Optional[int]] = mapped_column(Integer)  # Percentage
    rain_1h: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))  # mm
    rain_3h: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))  # mm
    snow_1h: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))  # mm
    snow_3h: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))  # mm
    
    # Observation timestamp
    observed_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    
    # Relationship
    location: Mapped["Location"] = relationship("Location", back_populates="current_weather")
    
    def get_weather_category(self) -> str:
        """Categorize weather for correlation analysis"""
        if not self.weather_condition:
            return "unknown"
        
        condition = self.weather_condition.lower()
        
        if any(word in condition for word in ["clear", "sunny"]):
            return "sunny"
        elif any(word in condition for word in ["rain", "drizzle", "shower"]):
            return "rainy"
        elif any(word in condition for word in ["cloud", "overcast"]):
            return "cloudy"
        elif any(word in condition for word in ["snow", "sleet"]):
            return "snowy"
        elif any(word in condition for word in ["storm", "thunder"]):
            return "stormy"
        elif any(word in condition for word in ["fog", "mist", "haze"]):
            return "foggy"
        else:
            return "other"
    
    def get_temperature_category(self) -> str:
        """Categorize temperature for correlation analysis"""
        if not self.temperature:
            return "unknown"
        
        temp = float(self.temperature)
        
        if temp >= 30:
            return "very_hot"    # 30°C+ / 86°F+
        elif temp >= 20:
            return "warm"        # 20-29°C / 68-84°F
        elif temp >= 10:
            return "mild"        # 10-19°C / 50-67°F
        elif temp >= 0:
            return "cool"        # 0-9°C / 32-49°F
        else:
            return "cold"        # Below 0°C / 32°F
    
    def is_precipitation(self) -> bool:
        """Check if there's any precipitation"""
        return any([
            self.rain_1h and self.rain_1h > 0,
            self.rain_3h and self.rain_3h > 0,
            self.snow_1h and self.snow_1h > 0,
            self.snow_3h and self.snow_3h > 0
        ])
    
    def __repr__(self):
        return f"<CurrentWeather(location_id='{self.location_id}', condition='{self.weather_condition}', temp={self.temperature})>"


class HistoricalWeather(BaseModel, CorrelationMixin, TimestampMixin):
    """
    Historical weather data for trend and seasonal correlation analysis
    """
    __tablename__ = 'historical_weather'
    __table_args__ = {'schema': 'weather'}
    
    # Location reference
    location_id: Mapped[str] = mapped_column(ForeignKey('weather.locations.id'))
    
    # Date for temporal correlation
    date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), index=True)
    
    # Daily temperature range
    temperature_min: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    temperature_max: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    temperature_avg: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    
    # Daily averages for correlation analysis
    humidity_avg: Mapped[Optional[int]] = mapped_column(Integer)
    pressure_avg: Mapped[Optional[int]] = mapped_column(Integer)
    wind_speed_avg: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    
    # Precipitation data
    precipitation: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))  # mm
    precipitation_hours: Mapped[Optional[int]] = mapped_column(Integer)  # hours with precipitation
    
    # Dominant weather condition for the day
    weather_condition: Mapped[Optional[str]] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String)
    
    # Sun and daylight data
    sunrise: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    sunset: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    daylight_hours: Mapped[Optional[Decimal]] = mapped_column(Numeric(4, 2))
    
    # Seasonal indicators
    season: Mapped[Optional[str]] = mapped_column(String(20))  # spring, summer, fall, winter
    
    # Relationship
    location: Mapped["Location"] = relationship("Location", back_populates="historical_weather")
    
    def get_season_from_date(self) -> str:
        """Determine season from date for correlation analysis"""
        if not self.date:
            return "unknown"
        
        month = self.date.month
        
        if month in [12, 1, 2]:
            return "winter"
        elif month in [3, 4, 5]:
            return "spring"
        elif month in [6, 7, 8]:
            return "summer"
        elif month in [9, 10, 11]:
            return "fall"
        else:
            return "unknown"
    
    def is_extreme_weather(self) -> bool:
        """Identify extreme weather days for correlation analysis"""
        if not self.temperature_min or not self.temperature_max:
            return False
        
        temp_min = float(self.temperature_min)
        temp_max = float(self.temperature_max)
        
        # Define extreme conditions
        extreme_hot = temp_max >= 35  # 35°C+ / 95°F+
        extreme_cold = temp_min <= -10  # -10°C / 14°F or lower
        extreme_precipitation = self.precipitation and self.precipitation >= 25  # 25mm+ / 1 inch+
        
        return any([extreme_hot, extreme_cold, extreme_precipitation])
    
    def __repr__(self):
        return f"<HistoricalWeather(location_id='{self.location_id}', date='{self.date}', condition='{self.weather_condition}')>"


class WeatherAlert(BaseModel, CorrelationMixin):
    """
    Weather alerts and warnings for correlation with behavioral changes
    """
    __tablename__ = 'weather_alerts'
    __table_args__ = {'schema': 'weather'}
    
    # Location reference
    location_id: Mapped[str] = mapped_column(ForeignKey('weather.locations.id'))
    
    # Alert information
    alert_type: Mapped[str] = mapped_column(String(100), nullable=False)  # tornado, flood, heat, etc.
    severity: Mapped[str] = mapped_column(String(50))  # minor, moderate, severe, extreme
    urgency: Mapped[str] = mapped_column(String(50))  # immediate, expected, future
    certainty: Mapped[str] = mapped_column(String(50))  # observed, likely, possible
    
    # Alert timing
    effective_time: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    expires_time: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))
    
    # Alert content
    headline: Mapped[Optional[str]] = mapped_column(String(500))
    description: Mapped[Optional[str]] = mapped_column(String)
    instruction: Mapped[Optional[str]] = mapped_column(String)
    
    # Areas affected (stored as JSON for complex geometries)
    affected_areas: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSONB)
    
    def is_active(self) -> bool:
        """Check if alert is currently active"""
        from datetime import datetime
        now = datetime.utcnow()
        
        if self.effective_time and self.expires_time:
            return self.effective_time <= now <= self.expires_time
        elif self.effective_time:
            return self.effective_time <= now
        else:
            return True  # No timing info, assume active
    
    def __repr__(self):
        return f"<WeatherAlert(location_id='{self.location_id}', type='{self.alert_type}', severity='{self.severity}')>"
