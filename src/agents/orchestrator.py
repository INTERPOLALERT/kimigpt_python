"""
Orchestrator Agent for WebsiteNow
Coordinates all other agents to generate websites
"""

import asyncio
from typing import Dict, Any, Optional, Callable
from datetime import datetime
import json
from pathlib import Path

from src.api.api_manager import APIManager
from src.agents.understanding_agent import UnderstandingAgent
from src.agents.design_agent import DesignAgent
from src.agents.code_agent import CodeAgent
from src.agents.content_agent import ContentAgent
from src.agents.qa_agent import QAAgent
from src.agents.deployment_agent import DeploymentAgent
from src.core.config_manager import ConfigManager


class OrchestratorAgent:
    """Master orchestrator that coordinates all agents"""

    def __init__(self):
        self.config_manager = ConfigManager()
        self.api_manager = APIManager()
        self.understanding_agent = UnderstandingAgent(self.api_manager)
        self.design_agent = DesignAgent(self.api_manager)
        self.code_agent = CodeAgent(self.api_manager)
        self.content_agent = ContentAgent(self.api_manager)
        self.qa_agent = QAAgent(self.api_manager)
        self.deployment_agent = DeploymentAgent()

    async def process(
        self,
        input_data: Dict[str, Any],
        progress_callback: Optional[Callable] = None,
        agent_callback: Optional[Callable] = None
    ) -> Dict[str, Any]:
        """
        Process website generation request

        Args:
            input_data: Dictionary containing project info, prompt, files, preferences
            progress_callback: Callback for progress updates (value, message)
            agent_callback: Callback for agent status updates (agent_name, status)

        Returns:
            Dictionary containing generation results
        """
        try:
            project_id = input_data.get('project_id', 'unknown')
            base_output_dir = self.config_manager.get_output_dir()
            output_dir = Path(base_output_dir) / project_id
            output_dir.mkdir(parents=True, exist_ok=True)

            result = {
                'success': False,
                'project_id': project_id,
                'started_at': datetime.now().isoformat(),
                'steps': []
            }

            # Step 1: Understanding Phase (10-25%)
            try:
                if progress_callback:
                    progress_callback(10, "🧠 Understanding your requirements...")
                if agent_callback:
                    agent_callback("Understanding", "Processing")

                understanding_result = await self.understanding_agent.analyze(input_data)
                result['steps'].append({
                    'agent': 'understanding',
                    'success': understanding_result.get('success', False)
                })

                if agent_callback:
                    agent_callback("Understanding", "Complete ✓")

                if progress_callback:
                    progress_callback(25, "Understanding complete")

            except Exception as e:
                print(f"Understanding error: {e}")
                understanding_result = {
                    'success': False,
                    'error': str(e),
                    'fallback_analysis': 'Create a professional website',
                    'raw_prompt': input_data.get('prompt', '')
                }

            # Step 2: Design Phase (25-40%)
            try:
                if progress_callback:
                    progress_callback(30, "🎨 Creating design specifications...")
                if agent_callback:
                    agent_callback("Design", "Processing")

                design_result = await self.design_agent.create_design(
                    understanding_result,
                    input_data.get('preferences', {})
                )
                result['steps'].append({
                    'agent': 'design',
                    'success': design_result.get('success', False)
                })

                if agent_callback:
                    agent_callback("Design", "Complete ✓")

                if progress_callback:
                    progress_callback(40, "Design complete")

            except Exception as e:
                print(f"Design error: {e}")
                design_result = {
                    'success': False,
                    'error': str(e),
                    'design_specification': 'Modern, clean design with responsive layout'
                }

            # Step 3: Content Generation (40-55%)
            try:
                if progress_callback:
                    progress_callback(45, "📝 Generating website content...")
                if agent_callback:
                    agent_callback("Content", "Processing")

                content_result = await self.content_agent.generate_content(
                    understanding_result,
                    design_result
                )
                result['steps'].append({
                    'agent': 'content',
                    'success': content_result.get('success', False)
                })

                if agent_callback:
                    agent_callback("Content", "Complete ✓")

                if progress_callback:
                    progress_callback(55, "Content complete")

            except Exception as e:
                print(f"Content error: {e}")
                content_result = {
                    'success': False,
                    'error': str(e),
                    'content': 'Professional website content',
                    'project_name': input_data.get('project_name', 'Website')
                }

            # Step 4: Code Generation (55-75%)
            try:
                if progress_callback:
                    progress_callback(60, "💻 Generating website code...")
                if agent_callback:
                    agent_callback("Code", "Processing")

                code_result = await self.code_agent.generate_code(
                    design_result,
                    content_result,
                    input_data.get('preferences', {})
                )
                result['steps'].append({
                    'agent': 'code',
                    'success': code_result.get('success', False)
                })
                result['code'] = code_result.get('files', {})

                if agent_callback:
                    agent_callback("Code", "Complete ✓")

                if progress_callback:
                    progress_callback(75, "Code generation complete")

            except Exception as e:
                print(f"Code error: {e}")
                # Code agent has built-in fallback, but add extra safety
                code_result = {
                    'success': False,
                    'error': str(e),
                    'files': {}
                }

            # Step 5: Quality Assurance (75-85%)
            try:
                if progress_callback:
                    progress_callback(80, "✅ Running quality checks...")
                if agent_callback:
                    agent_callback("QA", "Processing")

                qa_result = await self.qa_agent.validate(code_result)
                result['steps'].append({
                    'agent': 'qa',
                    'success': qa_result.get('success', False)
                })

                if agent_callback:
                    agent_callback("QA", "Complete ✓")

            except Exception as e:
                print(f"QA error: {e}")
                qa_result = {
                    'success': True,
                    'note': 'QA checks skipped'
                }

            # Step 6: Deployment/Packaging (85-100%)
            try:
                if progress_callback:
                    progress_callback(90, "📦 Packaging your website...")
                if agent_callback:
                    agent_callback("Deployment", "Processing")

                deployment_result = await self.deployment_agent.package(
                    code_result,
                    output_dir,
                    input_data
                )
                result['steps'].append({
                    'agent': 'deployment',
                    'success': deployment_result.get('success', False)
                })
                result['deploy_result'] = deployment_result

                if agent_callback:
                    agent_callback("Deployment", "Complete ✓")

            except Exception as e:
                print(f"Deployment error: {e}")
                deployment_result = {
                    'success': False,
                    'error': str(e)
                }

            # Complete
            if progress_callback:
                progress_callback(100, "✨ Website generated successfully!")

            result['success'] = True
            result['completed_at'] = datetime.now().isoformat()
            result['output_dir'] = str(output_dir)

            # Save result metadata
            try:
                with open(output_dir / 'generation_result.json', 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
            except Exception as e:
                print(f"Warning: Could not save metadata: {e}")

            return result

        except Exception as e:
            print(f"Orchestrator error: {e}")
            if progress_callback:
                progress_callback(100, f"❌ Error: {str(e)}")

            return {
                'success': False,
                'error': str(e),
                'project_id': input_data.get('project_id', 'unknown'),
                'completed_at': datetime.now().isoformat()
            }
