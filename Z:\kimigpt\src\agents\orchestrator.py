"""
Orchestrator Agent for KimiGPT
Coordinates all other agents to generate websites
"""

import asyncio
from typing import Dict, Any
from datetime import datetime
import os
import json
from pathlib import Path

from src.api.api_manager import APIManager
from src.agents.understanding_agent import UnderstandingAgent
from src.agents.design_agent import DesignAgent
from src.agents.code_agent import CodeAgent
from src.agents.content_agent import ContentAgent
from src.agents.qa_agent import QAAgent
from src.agents.deployment_agent import DeploymentAgent


class OrchestratorAgent:
    """Master orchestrator that coordinates all agents"""

    def __init__(self):
        self.api_manager = APIManager()
        self.understanding_agent = UnderstandingAgent(self.api_manager)
        self.design_agent = DesignAgent(self.api_manager)
        self.code_agent = CodeAgent(self.api_manager)
        self.content_agent = ContentAgent(self.api_manager)
        self.qa_agent = QAAgent(self.api_manager)
        self.deployment_agent = DeploymentAgent()

    async def process(self, input_data: Dict[str, Any], progress_callback=None, agent_callback=None) -> Dict[str, Any]:
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
            project_id = input_data['project_id']
            output_dir = Path(f"Z:\\kimigpt\\output\\{project_id}")
            output_dir.mkdir(parents=True, exist_ok=True)

            result = {
                'success': False,
                'project_id': project_id,
                'started_at': datetime.now().isoformat(),
                'steps': []
            }

            # Step 1: Understanding Phase
            if progress_callback:
                progress_callback(15, "Understanding your requirements...")
            if agent_callback:
                agent_callback("Understanding Agent", "Processing")

            understanding_result = await self.understanding_agent.analyze(input_data)
            result['steps'].append({'agent': 'understanding', 'result': understanding_result})

            if agent_callback:
                agent_callback("Understanding Agent", "Complete")

            # Step 2: Design Phase
            if progress_callback:
                progress_callback(30, "Creating design specifications...")
            if agent_callback:
                agent_callback("Design Agent", "Processing")

            design_result = await self.design_agent.create_design(
                understanding_result,
                input_data.get('preferences', {})
            )
            result['steps'].append({'agent': 'design', 'result': design_result})

            if agent_callback:
                agent_callback("Design Agent", "Complete")

            # Step 3: Content Generation
            if progress_callback:
                progress_callback(45, "Generating website content...")
            if agent_callback:
                agent_callback("Content Agent", "Processing")

            content_result = await self.content_agent.generate_content(
                understanding_result,
                design_result
            )
            result['steps'].append({'agent': 'content', 'result': content_result})

            if agent_callback:
                agent_callback("Content Agent", "Complete")

            # Step 4: Code Generation
            if progress_callback:
                progress_callback(60, "Generating website code...")
            if agent_callback:
                agent_callback("Code Agent", "Processing")

            code_result = await self.code_agent.generate_code(
                design_result,
                content_result,
                input_data.get('preferences', {})
            )
            result['steps'].append({'agent': 'code', 'result': code_result})
            result['code'] = code_result.get('files', {})

            if agent_callback:
                agent_callback("Code Agent", "Complete")

            # Step 5: Quality Assurance
            if progress_callback:
                progress_callback(75, "Running quality checks...")
            if agent_callback:
                agent_callback("QA Agent", "Processing")

            qa_result = await self.qa_agent.validate(code_result)
            result['steps'].append({'agent': 'qa', 'result': qa_result})

            if agent_callback:
                agent_callback("QA Agent", "Complete")

            # Step 6: Deployment/Packaging
            if progress_callback:
                progress_callback(90, "Packaging your website...")
            if agent_callback:
                agent_callback("Deployment Agent", "Processing")

            deployment_result = await self.deployment_agent.package(
                code_result,
                output_dir,
                input_data
            )
            result['steps'].append({'agent': 'deployment', 'result': deployment_result})
            result['deploy_result'] = deployment_result

            if agent_callback:
                agent_callback("Deployment Agent", "Complete")

            # Complete
            if progress_callback:
                progress_callback(100, "Website generated successfully!")

            result['success'] = True
            result['completed_at'] = datetime.now().isoformat()
            result['output_dir'] = str(output_dir)

            # Save result metadata
            with open(output_dir / 'generation_result.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            return result

        except Exception as e:
            if progress_callback:
                progress_callback(100, f"Error: {str(e)}")

            return {
                'success': False,
                'error': str(e),
                'project_id': input_data.get('project_id', 'unknown')
            }
