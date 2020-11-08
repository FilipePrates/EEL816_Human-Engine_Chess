using AsyncIO;
using NetMQ;
using NetMQ.Sockets;
using UnityEngine;

public class HelloClient : MonoBehaviour
{
    private RequestSocket _client;

    private void Start()
    {
        ForceDotNet.Force(); // this line is needed to prevent unity freeze after one use, not sure why yet
        _client = new RequestSocket();
        _client.Connect("tcp://localhost:5555");
    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            Debug.Log("Sending Hello");
            _client.SendFrame("Hello");
        }
        else if (Input.GetKeyDown(KeyCode.P))
        {
            Debug.Log("Sending printBoard");
            _client.SendFrame("printBoard");
        }
        else if (Input.GetKeyDown(KeyCode.L))
        {
            Debug.Log("Sending listen");
            _client.SendFrame("listen");
        }
        else if (Input.GetKeyDown(KeyCode.Escape))
        {
            Debug.Log("Sending endGame");
            _client.SendFrame("endGame");
        }
    }

    private void FixedUpdate()
    {
        if (!_client.HasIn)
        {
            return;
        }
        
        var gotMessage = _client.TryReceiveFrameString(out var message); // this returns true if it's successful
        if (!gotMessage)
        {
            return;
        }
        GameManager.instance.ProcessMessage(message);
        Debug.Log("Received " + message);
    }

    private void OnDestroy()
    {
        _client.Dispose();
        NetMQConfig.Cleanup(); // this line is needed to prevent unity freeze after one use, not sure why yet
    }
}