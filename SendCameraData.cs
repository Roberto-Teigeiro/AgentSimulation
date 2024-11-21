using UnityEngine;
using System.Collections;
using UnityEngine.Networking;
using System.IO;

public class CameraCapture : MonoBehaviour
{
    public string serverUrl = "http://127.0.0.1:5000/upload_image"; // Flask server endpoint
    public string cameraName = "SecurityAgent"; // The name of the camera in the scene

    private Camera cameraToCapture;

    void Start()
    {
        // Get the camera by its name
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

            // Send image data to Flask server
            UnityWebRequest request = new UnityWebRequest(serverUrl, "POST");
            byte[] jsonToSend = new System.Text.UTF8Encoding().GetBytes("{\"image\":\"" + base64Image + "\"}");
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

            yield return new WaitForSeconds(0.1f); // Send an image every 0.1s (10 FPS)
        }
    }
}
