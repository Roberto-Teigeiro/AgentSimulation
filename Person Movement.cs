using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

public class AgentController : MonoBehaviour
{
    public string serverUrl = "http://127.0.0.1:5000/position"; // Flask server endpoint
    public float updateInterval = 0.1f;  // How often to fetch data (in seconds)
    public float radius = 5f;  // Radius of the circle the agent will move in
    public float speed = 1f;   // Speed of movement around the circle
    public float cameraDistance = 10f; // Camera's initial distance from the agent

    private Vector3 agentPosition;
    private float agentAngle;
    private float height = 2f; // Height offset for the agent

    void Start()
    {
        StartCoroutine(UpdateAgentPosition());
    }

    IEnumerator UpdateAgentPosition()
    {
        while (true)
        {
            UnityWebRequest request = UnityWebRequest.Get(serverUrl);
            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.Success)
            {
                string json = request.downloadHandler.text;
                PositionData positionData = JsonUtility.FromJson<PositionData>(json);

                // Update agent's position and rotation
                agentPosition = new Vector3(positionData.x, height, positionData.z);  // Y is constant (height)
                transform.position = agentPosition;

                agentAngle = positionData.angle;  // Retrieve angle
                transform.rotation = Quaternion.Euler(0, agentAngle, 0);  // Rotate around Y-axis for agent
            }
            else
            {
                Debug.LogError("Error fetching position: " + request.error);
            }

            yield return new WaitForSeconds(updateInterval);
        }
    }

    [System.Serializable]
    public class PositionData
    {
        public float x;    // X-coordinate of the agent
        public float z;    // Z-coordinate of the agent
        public float angle; // Angle (in degrees) of the agent
    }
}
