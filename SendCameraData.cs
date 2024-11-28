// CameraCapture.cs
using UnityEngine;
using System.Collections;
using UnityEngine.Networking;
using System.IO;

public class CameraCapture : MonoBehaviour
{
    [Header("Server Settings")]
    [Tooltip("Base URL of the Flask server (e.g., http://localhost:5000)")]
    public string serverBaseUrl = "http://127.0.0.1:5000"; // Flask server base URL

    [Header("Agent Settings")]
    [Tooltip("Type of the agent (e.g., Drone, Robber, Camera)")]
    public string agentType = "SecurityAgent"; // Assign this in the Inspector

    [Header("Camera Settings")]
    [Tooltip("The name of the camera in the scene")]
    public string cameraName = "SecurityAgent"; // The name of the camera in the scene

    private Camera cameraToCapture;

    void Start()
    {
        cameraToCapture = GameObject.Find(cameraName).GetComponent<Camera>();

        if (cameraToCapture == null)
        {
            Debug.LogError("Camera not found. Please make sure the camera name is correct.");
            return;
        }

        // Start capturing and sending the image
        StartCoroutine(CaptureAndSendImage());
    }

    IEnumerator CaptureAndSendImage()
    {
        while (true)
        {
            // Create a RenderTexture to capture the camera's view
            RenderTexture renderTexture = new RenderTexture(1920, 1080, 24);
            cameraToCapture.targetTexture = renderTexture;
            cameraToCapture.Render();

            // Create a Texture2D to hold the captured image
            Texture2D texture = new Texture2D(renderTexture.width, renderTexture.height, TextureFormat.RGB24, false);
            RenderTexture.active = renderTexture;
            texture.ReadPixels(new Rect(0, 0, renderTexture.width, renderTexture.height), 0, 0);
            texture.Apply();

            // Encode texture to PNG
            byte[] imageBytes = texture.EncodeToPNG();
            string base64Image = System.Convert.ToBase64String(imageBytes);

            // Prepare JSON payload
            string filename = $"{agentType}_vision.png";
            ImagePayload payload = new ImagePayload
            {
                image = base64Image,
                filename = filename
            };
            string jsonPayload = JsonUtility.ToJson(payload);

            // Construct the server URL with agentType
            string url = $"{serverBaseUrl}/send_vision/{agentType}";

            // Send image data to Flask server
            UnityWebRequest request = new UnityWebRequest(url, "POST");
            byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes(jsonPayload);
            request.uploadHandler = new UploadHandlerRaw(jsonToSend);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");

            yield return request.SendWebRequest();

            if (request.result == UnityWebRequest.Result.Success)
            {
                Debug.Log("Image sent successfully.");
            }
            else
            {
                Debug.LogError("Error sending image: " + request.error);
            }

            // Clean up
            cameraToCapture.targetTexture = null;
            RenderTexture.active = null;
            Destroy(renderTexture);
            Destroy(texture);

            yield return new WaitForSeconds(0.1f); // Send an image every 0.1s (10 FPS)
        }
    }

    [System.Serializable]
    public class ImagePayload
    {
        public string image;
        public string filename;
    }
}