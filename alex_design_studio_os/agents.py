from .base import AgentSpec, BaseAgent


class AlexAIAssistant(BaseAgent):
    spec = AgentSpec(key="AlexAIAssistant", name="AlexAIAssistant", category="Core Intelligence", responsibility='Understand user instructions, collect a client brief, and route work.')

class AlexAIDirector(BaseAgent):
    spec = AgentSpec(key="AlexAIDirector", name="AlexAIDirector", category="Core Intelligence", responsibility='Plan creative workflows and coordinate agent execution.')

class CreativeIntelligenceAgent(BaseAgent):
    spec = AgentSpec(key="CreativeIntelligenceAgent", name="CreativeIntelligenceAgent", category="Core Intelligence", responsibility='Generate creative directions and campaign opportunities.')

class ClientBriefAnalyzer(BaseAgent):
    spec = AgentSpec(key="ClientBriefAnalyzer", name="ClientBriefAnalyzer", category="Research & Planning", responsibility='Extract business, product, audience, goal, language, and deliverables from a brief.')

class TrendAnalysisAgent(BaseAgent):
    spec = AgentSpec(key="TrendAnalysisAgent", name="TrendAnalysisAgent", category="Research & Planning", responsibility='Identify trend hypotheses and mark current-trend claims for live verification.')

class ResearchAgent(BaseAgent):
    spec = AgentSpec(key="ResearchAgent", name="ResearchAgent", category="Research & Planning", responsibility='Organize research questions, references, and evidence requirements.')

class DesignRecommendationEngine(BaseAgent):
    spec = AgentSpec(key="DesignRecommendationEngine", name="DesignRecommendationEngine", category="Research & Planning", responsibility='Recommend visual approaches suited to the brief.')

class CreativeStrategyAgent(BaseAgent):
    spec = AgentSpec(key="CreativeStrategyAgent", name="CreativeStrategyAgent", category="Research & Planning", responsibility='Build a coherent campaign strategy.')

class AudienceIntelligenceAgent(BaseAgent):
    spec = AgentSpec(key="AudienceIntelligenceAgent", name="AudienceIntelligenceAgent", category="Research & Planning", responsibility='Describe audience needs and likely motivations from supplied information.')

class CampaignPlannerAgent(BaseAgent):
    spec = AgentSpec(key="CampaignPlannerAgent", name="CampaignPlannerAgent", category="Research & Planning", responsibility='Plan campaign assets and sequence.')

class ContentCalendarAgent(BaseAgent):
    spec = AgentSpec(key="ContentCalendarAgent", name="ContentCalendarAgent", category="Research & Planning", responsibility='Draft a content calendar.')

class AIArtDirector(BaseAgent):
    spec = AgentSpec(key="AIArtDirector", name="AIArtDirector", category="Graphic Design", responsibility='Set visual direction and composition.')

class GraphicDesignerAgent(BaseAgent):
    spec = AgentSpec(key="GraphicDesignerAgent", name="GraphicDesignerAgent", category="Graphic Design", responsibility='Prepare design specifications for posters, banners, and social creatives.')

class LayoutAgent(BaseAgent):
    spec = AgentSpec(key="LayoutAgent", name="LayoutAgent", category="Graphic Design", responsibility='Define hierarchy, grid, spacing, and composition.')

class TypographyAgent(BaseAgent):
    spec = AgentSpec(key="TypographyAgent", name="TypographyAgent", category="Graphic Design", responsibility='Recommend typography hierarchy.')

class ColorIntelligenceAgent(BaseAgent):
    spec = AgentSpec(key="ColorIntelligenceAgent", name="ColorIntelligenceAgent", category="Graphic Design", responsibility='Recommend color palettes and usage.')

class ImageSelectionAgent(BaseAgent):
    spec = AgentSpec(key="ImageSelectionAgent", name="ImageSelectionAgent", category="Graphic Design", responsibility='Specify image selection criteria and asset needs.')

class IllustrationAgent(BaseAgent):
    spec = AgentSpec(key="IllustrationAgent", name="IllustrationAgent", category="Graphic Design", responsibility='Plan illustration concepts.')

class BackgroundTextureAgent(BaseAgent):
    spec = AgentSpec(key="BackgroundTextureAgent", name="BackgroundTextureAgent", category="Graphic Design", responsibility='Specify backgrounds and textures.')

class MockupAgent(BaseAgent):
    spec = AgentSpec(key="MockupAgent", name="MockupAgent", category="Graphic Design", responsibility='Plan product and brand mockups.')

class ThreeDDesignAgent(BaseAgent):
    spec = AgentSpec(key="ThreeDDesignAgent", name="ThreeDDesignAgent", category="Graphic Design", responsibility='Plan 3D visual concepts.')

class MarathiTypographyAgent(BaseAgent):
    spec = AgentSpec(key="MarathiTypographyAgent", name="MarathiTypographyAgent", category="Graphic Design", responsibility='Flag Devanagari layout, font, and rendering requirements.')

class DesignAdaptationAgent(BaseAgent):
    spec = AgentSpec(key="DesignAdaptationAgent", name="DesignAdaptationAgent", category="Graphic Design", responsibility='Adapt design requirements to multiple formats.')

class AdvertisingConceptAgent(BaseAgent):
    spec = AgentSpec(key="AdvertisingConceptAgent", name="AdvertisingConceptAgent", category="Advertising & Marketing", responsibility='Create an ad concept with headline, visual direction, formats, and CTA.')

class AICopywriterAgent(BaseAgent):
    spec = AgentSpec(key="AICopywriterAgent", name="AICopywriterAgent", category="Advertising & Marketing", responsibility='Draft headlines, captions, and advertising copy.')

class BrandStrategistAgent(BaseAgent):
    spec = AgentSpec(key="BrandStrategistAgent", name="BrandStrategistAgent", category="Advertising & Marketing", responsibility='Define positioning and brand message from supplied facts.')

class BrandConsistencyAgent(BaseAgent):
    spec = AgentSpec(key="BrandConsistencyAgent", name="BrandConsistencyAgent", category="Advertising & Marketing", responsibility='Check supplied brand guidelines and identify missing information.')

class SocialMediaManagerAgent(BaseAgent):
    spec = AgentSpec(key="SocialMediaManagerAgent", name="SocialMediaManagerAgent", category="Advertising & Marketing", responsibility='Plan social posts and content formats.')

class AdCampaignAgent(BaseAgent):
    spec = AgentSpec(key="AdCampaignAgent", name="AdCampaignAgent", category="Advertising & Marketing", responsibility='Create campaign variations and rollout suggestions.')

class CTAOptimizationAgent(BaseAgent):
    spec = AgentSpec(key="CTAOptimizationAgent", name="CTAOptimizationAgent", category="Advertising & Marketing", responsibility='Suggest calls to action aligned with campaign goals.')

class MarketingAnalystAgent(BaseAgent):
    spec = AgentSpec(key="MarketingAnalystAgent", name="MarketingAnalystAgent", category="Advertising & Marketing", responsibility='Define campaign metrics and analysis plan.')

class PricingAssistantAgent(BaseAgent):
    spec = AgentSpec(key="PricingAssistantAgent", name="PricingAssistantAgent", category="Advertising & Marketing", responsibility='Structure draft service pricing; require owner approval.')

class PromptEngineeringAgent(BaseAgent):
    spec = AgentSpec(key="PromptEngineeringAgent", name="PromptEngineeringAgent", category="AI Image, Video & Motion", responsibility='Convert a creative direction into a structured generation prompt.')

class ImageGenerationAgent(BaseAgent):
    spec = AgentSpec(key="ImageGenerationAgent", name="ImageGenerationAgent", category="AI Image, Video & Motion", responsibility='Prepare an image-generation request; provider execution requires integration.')

class ImageEditingAgent(BaseAgent):
    spec = AgentSpec(key="ImageEditingAgent", name="ImageEditingAgent", category="AI Image, Video & Motion", responsibility='Specify edits to an existing image.')

class ProductPhotographyAgent(BaseAgent):
    spec = AgentSpec(key="ProductPhotographyAgent", name="ProductPhotographyAgent", category="AI Image, Video & Motion", responsibility='Plan product photography lighting, composition, and styling.')

class FoodAdvertisingAgent(BaseAgent):
    spec = AgentSpec(key="FoodAdvertisingAgent", name="FoodAdvertisingAgent", category="AI Image, Video & Motion", responsibility='Plan food advertising visuals and appetizing composition.')

class AIVideoDirectorAgent(BaseAgent):
    spec = AgentSpec(key="AIVideoDirectorAgent", name="AIVideoDirectorAgent", category="AI Image, Video & Motion", responsibility='Plan scenes, timing, transitions, and narrative.')

class VideoGenerationAgent(BaseAgent):
    spec = AgentSpec(key="VideoGenerationAgent", name="VideoGenerationAgent", category="AI Image, Video & Motion", responsibility='Prepare a video-generation job; provider execution requires integration.')

class MotionGraphicsAgent(BaseAgent):
    spec = AgentSpec(key="MotionGraphicsAgent", name="MotionGraphicsAgent", category="AI Image, Video & Motion", responsibility='Specify motion graphics and animation behavior.')

class SceneContinuityAgent(BaseAgent):
    spec = AgentSpec(key="SceneContinuityAgent", name="SceneContinuityAgent", category="AI Image, Video & Motion", responsibility='Check continuity requirements between scenes.')

class VoiceAudioAgent(BaseAgent):
    spec = AgentSpec(key="VoiceAudioAgent", name="VoiceAudioAgent", category="AI Image, Video & Motion", responsibility='Plan voiceover, music, and audio cues.')

class VideoEditingAgent(BaseAgent):
    spec = AgentSpec(key="VideoEditingAgent", name="VideoEditingAgent", category="AI Image, Video & Motion", responsibility='Plan edit timing, transitions, and final assembly.')

class DesignQAAgent(BaseAgent):
    spec = AgentSpec(key="DesignQAAgent", name="DesignQAAgent", category="Quality, Security & Delivery", responsibility='Check deliverables against a supplied checklist.')

class AIDesignCritic(BaseAgent):
    spec = AgentSpec(key="AIDesignCritic", name="AIDesignCritic", category="Quality, Security & Delivery", responsibility='Identify possible weaknesses and propose improvements.')

class BrandComplianceAgent(BaseAgent):
    spec = AgentSpec(key="BrandComplianceAgent", name="BrandComplianceAgent", category="Quality, Security & Delivery", responsibility='Check outputs against supplied brand rules.')

class AssetLicensingAgent(BaseAgent):
    spec = AgentSpec(key="AssetLicensingAgent", name="AssetLicensingAgent", category="Quality, Security & Delivery", responsibility='Require provenance and license review for assets.')

class SecurityAgent(BaseAgent):
    spec = AgentSpec(key="SecurityAgent", name="SecurityAgent", category="Quality, Security & Delivery", responsibility='Check security practices and avoid exposing secrets.')

class LocalizationAgent(BaseAgent):
    spec = AgentSpec(key="LocalizationAgent", name="LocalizationAgent", category="Quality, Security & Delivery", responsibility='Plan Marathi, Hindi, and English localization.')

class ExportAgent(BaseAgent):
    spec = AgentSpec(key="ExportAgent", name="ExportAgent", category="Quality, Security & Delivery", responsibility='Specify export formats and dimensions.')

class ClientDeliveryAgent(BaseAgent):
    spec = AgentSpec(key="ClientDeliveryAgent", name="ClientDeliveryAgent", category="Quality, Security & Delivery", responsibility='Organize delivery package and handoff checklist.')

class RevisionAgent(BaseAgent):
    spec = AgentSpec(key="RevisionAgent", name="RevisionAgent", category="Quality, Security & Delivery", responsibility='Turn client feedback into a revision checklist.')

class PerformanceAnalyticsAgent(BaseAgent):
    spec = AgentSpec(key="PerformanceAnalyticsAgent", name="PerformanceAnalyticsAgent", category="Quality, Security & Delivery", responsibility='Define performance metrics and reporting plan.')

class FeedbackLearningAgent(BaseAgent):
    spec = AgentSpec(key="FeedbackLearningAgent", name="FeedbackLearningAgent", category="Quality, Security & Delivery", responsibility='Convert approved feedback into explicit future guidelines.')

class ClientManagementAgent(BaseAgent):
    spec = AgentSpec(key="ClientManagementAgent", name="ClientManagementAgent", category="Business & System", responsibility='Structure client and project metadata.')

class ProjectManagementAgent(BaseAgent):
    spec = AgentSpec(key="ProjectManagementAgent", name="ProjectManagementAgent", category="Business & System", responsibility='Break work into tasks and checkpoints.')

class WorkflowOrchestratorAgent(BaseAgent):
    spec = AgentSpec(key="WorkflowOrchestratorAgent", name="WorkflowOrchestratorAgent", category="Business & System", responsibility='Sequence agent tasks and collect outputs.')

class JobMonitoringAgent(BaseAgent):
    spec = AgentSpec(key="JobMonitoringAgent", name="JobMonitoringAgent", category="Business & System", responsibility='Report local job state; external worker integration is separate.')

class ErrorRecoveryAgent(BaseAgent):
    spec = AgentSpec(key="ErrorRecoveryAgent", name="ErrorRecoveryAgent", category="Business & System", responsibility='Classify failures and recommend safe recovery actions.')

class AssetPipelineAgent(BaseAgent):
    spec = AgentSpec(key="AssetPipelineAgent", name="AssetPipelineAgent", category="Business & System", responsibility='Organize asset intake, processing, and output paths.')

class PluginRegistryAgent(BaseAgent):
    spec = AgentSpec(key="PluginRegistryAgent", name="PluginRegistryAgent", category="Business & System", responsibility='Describe provider/plugin registrations.')

class SystemHealthAgent(BaseAgent):
    spec = AgentSpec(key="SystemHealthAgent", name="SystemHealthAgent", category="Business & System", responsibility='Report local runtime and dependency checks.')

class CostMonitoringAgent(BaseAgent):
    spec = AgentSpec(key="CostMonitoringAgent", name="CostMonitoringAgent", category="Business & System", responsibility='Define cost tracking fields; real costs require provider usage data.')

class AutonomousCreativeDirector(BaseAgent):
    spec = AgentSpec(key="AutonomousCreativeDirector", name="AutonomousCreativeDirector", category="Business & System", responsibility='Supervise the creative plan and flag decisions needing human approval.')
