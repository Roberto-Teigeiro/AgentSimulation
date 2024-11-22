using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using Newtonsoft.Json;

public class PersonMovement : MonoBehaviour
{
    [Header("Server Settings")]
    [Tooltip("Base URL of the Flask server (e.g., http://localhost:5000)")]
    public string serverBaseUrl = "http://localhost:5000";

    [Header("Fetch Settings")]
    [Tooltip("Interval in seconds between each fetch")]
    public float fetchInterval = 1f;

    [Header("Movement Settings")]
    [Tooltip("Speed at which the GameObject moves towards the target position")]
    public float moveSpeed = 5f;

    [Header("Agent Settings")]
    [Tooltip("Type of the agent (e.g., Drone, Robber, Camera)")]
    public string agentType; // Assign this in the Inspector for each GameObject

    private Vector3 targetPosition;

    void Start()
    {
        if (string.IsNullOrEmpty(agentType))
        {
            Debug.LogError($"agentType not set for GameObject '{gameObject.name}'. Please assign an agent type in the Inspector.");
            enabled = false; // Disable the script to prevent errors
            return;
        }

        // Initialize targetPosition to the current position at start
        targetPosition = transform.position;

        StartCoroutine(FetchPositionRoutine());
    }

    /// <summary>
    /// Coroutine to periodically fetch the agent's position from the server.
    /// </summary>
    IEnumerator FetchPositionRoutine()
    {
        while (true)
        {
            yield return StartCoroutine(FetchPosition());
            yield return new WaitForSeconds(fetchInterval);
        }
    }

    /// <summary>
    /// Sends a GET request to fetch the agent's current position.
    /// </summary>
    /// <returns></returns>
    IEnumerator FetchPosition()
    {
        string url = $"{serverBaseUrl}/get_position/{agentType}";
        UnityWebRequest request = UnityWebRequest.Get(url);
        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
        {
            string jsonResponse = request.downloadHandler.text;

            try
            {
                Position pos = JsonConvert.DeserializeObject<Position>(jsonResponse);

                // Set the new target position instead of directly updating the transform
                targetPosition = new Vector3(pos.x, transform.position.y, pos.y); // Map y to z

                Debug.Log($"{agentType} position updated to: {targetPosition}");
            }
            catch (JsonException e)
            {
                Debug.LogError($"JSON Deserialization Error: {e.Message}");
                Debug.LogError($"Received JSON: {jsonResponse}");
            }
        }
        else
        {
            Debug.LogError($"Failed to fetch position for '{agentType}': {request.error}");
        }
    }

    void Update()
    {
        // Smoothly move towards the target position
        transform.position = Vector3.Lerp(transform.position, targetPosition, moveSpeed * Time.deltaTime);
    }
}

[System.Serializable]
public class Position
{
    public float x;
    public float y;
}