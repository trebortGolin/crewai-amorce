"""
Basic CrewAI-Amorce Example

Shows how to secure a CrewAI crew with 1 decorator.
"""

from crewai import Crew, Agent, Task
from crewai_amorce import secure_crew

def main():
    print("🔐 CrewAI-Amorce Basic Example\n")
    
    # Define agents
    researcher = Agent(
        role='Senior Researcher',
        goal='Uncover cutting-edge developments in AI',
        backstory='You are a renowned AI researcher',
        verbose=True
    )
    
    writer = Agent(
        role='Tech Writer',
        goal='Create comprehensive technical reports',
        backstory='You are an award-winning tech writer',
        verbose=True
    )
    
    # Define tasks
    research_task = Task(
        description='Research latest AI agent developments',
        agent=researcher
    )
    
    write_task = Task(
        description='Write a report on AI agent security',
        agent=writer
    )
    
    # Secure the crew (1 decorator!)
    print("Creating secure crew...")
    
    @secure_crew(verbose=True)
    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        verbose=True
    )
    
    print(f"✅ Crew secured with ID: {crew.crew_id}\n")
    
    # Run the crew
    print("Starting crew kickoff...")
    result = crew.kickoff()
    
    print(f"\nResult: {result['result']}")
    print(f"\nSecurity Metadata:")
    print(f"  Crew ID: {result['crew_id']}")
    print(f"  Signature: {result['signature'][:50]}...")
    print(f"  Protocol: {result['protocol']}")
    print(f"  Security Layer: {result['security_layer']}")

if __name__ == "__main__":
    main()
