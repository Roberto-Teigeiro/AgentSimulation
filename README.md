# Evidence 2 - Intermediate Delivery
Link to Unity assets and world: https://drive.google.com/drive/folders/1D504VsSRE-t0EKTkW0W09vwq0rtGZ9k1
## Modeling of Multi-Agent Systems with Computer Graphics (Gpo 301)
This information is also found in .pdf file in repository
This is part of the final delivarable evidence
**Evidence 2 - Final Deliverable**

### Students:
- Omar Michel Carmona Villalobos | A01644146  
- Roberto Anwar Teigeiro Aguilar | A01643651  
- Luis Omar Olmedo Ortiz | A01643557  
- Catalina Pesquet | A01763937  
- Andres Barrera | A01763911  

### Professors:
- Iván Axel Dounce Nava  
- Carlos Johnnatan Sandoval Arrayga  
- Obed Nehemías Muñoz Reynoso  

**Guadalajara, Jalisco**  
**November 2024**

---

## 1. Problem Description

This project addresses the challenge of coordinated patrolling in high-risk, resource-sensitive environments. By leveraging a multi-agent system, the simulation integrates drones, fixed cameras, and security personnel to form a robust surveillance network. The system detects and responds to potential threats such as unauthorized intrusions or suspicious activities, ensuring rapid and effective incident resolution. The simulation applies principles of artificial intelligence, inter-agent communication, and autonomous systems for enhanced safety in real-world scenarios like factories and agricultural areas.

---

## 2. Agents Description

### 2.1 **DronAgent**
- **setup()**: Initializes attributes and BDI architecture.  
- **See(Environment)**: Detects robbers within a range (10 units).  
- **Brf(Detected_robber)**: Updates beliefs with detected robber positions.  
- **Options()**: Generates goals based on beliefs.  
- **Filter()**: Selects relevant goals (e.g., inspecting robbers).  
- **Plan()**: Creates a path to a robber's position.  
- **Execute()**: Executes the plan step-by-step.  
- **Takeoff()**: Simulates drone takeoff.  
- **Land()**: Simulates drone landing.  
- **Step()**: Implements the BDI cycle, handling perception, planning, and execution.

### 2.2 **RobberAgent**
- **setup()**: Initializes attributes.  
- **move_randomly()**: Generates random movements.  
- **step()**: Updates the robber’s behavior each simulation step.

### 2.3 **CamaraAgent**
- **setup()**: Initializes with detection range (20 units) and alert counter.  
- **detect_robber()**: Detects robbers in range.  
- **send_alert(robber)**: Sends alerts and increments alert count.  
- **step()**: Detects and alerts if robbers are found.

### 2.4 **SecurityPersonnelAgent**
- **setup()**: Initializes communication and alert resolution attributes.  
- **respond_to_drone_signal(drone, robber_position)**: Assists drones in confirming robber presence.  
- **confirm_robber(drone, robber_position)**: Validates robber existence and escalates with a general alarm.  
- **simulate_general_alarm(drone)**: Issues alarms and updates alert status.  
- **step()**: Monitors alerts and coordinates responses.

---

## 3. Ontology

### 3.1 Core Classes
- **Entity (Thing)**: Base class for all agents and entities.  
- **Drone (Entity)**: Represents patrolling drones.  
- **Camera (Entity)**: Represents stationary surveillance cameras.  
- **Robber (Entity)**: Represents suspicious individuals.  
- **SecurityPersonnel (Entity)**: Manages threats and coordinates drones.  
- **Place (Thing)**: Represents areas of interest.

### 3.2 Relationships
- **is_in_place**: Links entities to places.  
- **at_position**: Specifies the location of places.  
- **detects_suspicion**: Links cameras/drones to detected robbers.  
- **alerts**: Links cameras to drones or security personnel.  
- **patrolled_by**: Links drones to their patrol areas.  
- **status**: Tracks entity status.

---

## 4. Agent Classes and Protocol Diagram

### Diagram Overview:
1. **Entity Hierarchy**: Abstract `Thing` class forms the base for all entities.  
2. **Agent Classes**:  
   - **Drone**: Autonomous surveillance agent.  
   - **Camera**: Detects and alerts about robbers.  
   - **Robber**: Suspicious individual moving randomly.  
   - **SecurityPersonnel**: Responds to alerts and confirms threats.  
   - **Place**: Represents locations.  
3. **Relationships**: Models inter-agent and agent-place interactions.  
4. **Data Properties**: Tracks positional and status information.

---

## 5. Tasks for Final Delivery:
- **Documentation**: Due Friday, November 29th by Omar Michel and Luis Omar.  
- **Agent Training**: Due Wednesday, November 27th by Roberto.  
- **Unity Environment**: Enhancements due Wednesday, November 27th by Andres.  
- **Agent Code Improvements**: Due Thursday, November 28th by Catalina.  
- **Presentation Preparation**: Due Thursday, November 28th by all team members.

---

## 6. Analysis and Reflections

WIP
---

