import asyncio
from typing import Dict, Any, List
from datetime import datetime
import json
from src.agents.base_agent import BaseAgent
from src.agents.understanding_agent import UnderstandingAgent
from src.agents.design_agent import DesignAgent
from src.agents.code_agent import CodeAgent
from src.agents.image_agent import ImageAgent
from src.agents.content_agent import ContentAgent
from src.agents.qa_agent import QAAgent
from src.agents.deployment_agent import DeploymentAgent

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Master Orchestrator", "orchestrator_001")
        
        # Initialize all specialized agents
        self.agents = {
            'understanding': UnderstandingAgent(),
            'design': DesignAgent(),
            'code': CodeAgent(),
            'image': ImageAgent(),
            'content': ContentAgent(),
            'qa': QAAgent(),
            'deployment': DeploymentAgent()
        }
        
        self.project_data = {}
        self.generation_history = []
        self.current_project_id = None
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate the entire website generation process"""
        self.update_status("processing")
        self.current_project_id = input_data.get('project_id', f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        
        try:
            # Step 1: Understanding Phase
            self.log_activity("Starting understanding phase...")
            understanding_result = await self.agents['understanding'].process(input_data)
            self.project_data.update(understanding_result)
            
            # Step 2: Design Phase
            self.log_activity("Starting design phase...")
            design_input = {
                'requirements': understanding_result,
                'user_preferences': input_data.get('preferences', {}),
                'uploaded_images': input_data.get('images', [])
            }
            design_result = await self.agents['design'].process(design_input)
            self.project_data['design'] = design_result
            
            # Step 3: Image Processing (if images uploaded)
            if input_data.get('images'):
                self.log_activity("Processing uploaded images...")
                image_input = {
                    'images': input_data['images'],
                    'design_spec': design_result
                }
                image_result = await self.agents['image'].process(image_input)
                self.project_data['images'] = image_result
            
            # Step 4: Content Generation
            self.log_activity("Generating content...")
            content_input = {
                'requirements': understanding_result,
                'design_spec': design_result,
                'project_type': self.project_data.get('project_type', 'website')
            }
            content_result = await self.agents['content'].process(content_input)
            self.project_data['content'] = content_result
            
            # Step 5: Code Generation
            self.log_activity("Generating code...")
            code_input = {
                'design': design_result,
                'content': content_result,
                'images': self.project_data.get('images', {}),
                'requirements': understanding_result,
                'framework': input_data.get('framework', 'vanilla'),
                'complexity': input_data.get('complexity', 'moderate')
            }
            code_result = await self.agents['code'].process(code_input)
            self.project_data['code'] = code_result
            
            # Step 6: Quality Assurance
            self.log_activity("Running quality assurance...")
            qa_input = {
                'code': code_result,
                'design': design_result,
                'requirements': understanding_result
            }
            qa_result = await self.agents['qa'].process(qa_input)
            
            # If QA fails, regenerate
            if not qa_result.get('passed', False):
                self.log_activity("QA failed, regenerating...")
                # Add QA feedback to code generation
                code_input['qa_feedback'] = qa_result.get('feedback', [])
                code_result = await self.agents['code'].process(code_input)
                self.project_data['code'] = code_result
                
                # Re-run QA
                qa_result = await self.agents['qa'].process(qa_input)
            
            # Step 7: Deployment Preparation
            self.log_activity("Preparing deployment...")
            deploy_input = {
                'code': code_result,
                'project_id': self.current_project_id,
                'project_name': input_data.get('project_name', 'My Website'),
                'user_preferences': input_data.get('preferences', {})
            }
            deploy_result = await self.agents['deployment'].process(deploy_input)
            self.project_data['deployment'] = deploy_result
            
            # Save to history
            self.generation_history.append({
                'project_id': self.current_project_id,
                'timestamp': datetime.now(),
                'input': input_data,
                'output': self.project_data
            })
            
            self.update_status("completed")
            
            return {
                'success': True,
                'project_id': self.current_project_id,
                'project_data': self.project_data,
                'qa_result': qa_result,
                'deploy_result': deploy_result,
                'generation_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            self.log_activity(f"Orchestration failed: {str(e)}", "error")
            self.update_status("error")
            return {
                'success': False,
                'error': str(e),
                'project_id': self.current_project_id
            }
    
    async def regenerate_component(self, component: str, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """Regenerate a specific component with feedback"""
        self.update_status("regenerating")
        
        try:
            if component == 'design':
                design_input = {
                    'requirements': self.project_data.get('requirements', {}),
                    'user_preferences': feedback.get('preferences', {}),
                    'feedback': feedback.get('design_feedback', [])
                }
                result = await self.agents['design'].process(design_input)
                self.project_data['design'] = result
                
            elif component == 'code':
                code_input = {
                    'design': self.project_data.get('design', {}),
                    'content': self.project_data.get('content', {}),
                    'images': self.project_data.get('images', {}),
                    'requirements': self.project_data.get('requirements', {}),
                    'feedback': feedback.get('code_feedback', [])
                }
                result = await self.agents['code'].process(code_input)
                self.project_data['code'] = result
                
            elif component == 'content':
                content_input = {
                    'requirements': self.project_data.get('requirements', {}),
                    'design_spec': self.project_data.get('design', {}),
                    'feedback': feedback.get('content_feedback', [])
                }
                result = await self.agents['content'].process(content_input)
                self.project_data['content'] = result
            
            # Re-run QA for the regenerated component
            qa_input = {
                'code': self.project_data.get('code', {}),
                'design': self.project_data.get('design', {}),
                'requirements': self.project_data.get('requirements', {})
            }
            qa_result = await self.agents['qa'].process(qa_input)
            
            self.update_status("completed")
            
            return {
                'success': True,
                'component': component,
                'result': result,
                'qa_result': qa_result
            }
            
        except Exception as e:
            self.log_activity(f"Regeneration failed for {component}: {str(e)}", "error")
            self.update_status("error")
            return {
                'success': False,
                'error': str(e),
                'component': component
            }
    
    def get_project_history(self) -> List[Dict[str, Any]]:
        """Get generation history"""
        return self.generation_history
    
    def get_current_project(self) -> Dict[str, Any]:
        """Get current project data"""
        return self.project_data
    
    async def cleanup(self):
        """Cleanup all agents"""
        for agent in self.agents.values():
            await agent.cleanup()
        self.update_status("idle")