// By Tiger3018 2022/06/15, MIT License
using System.Collections;
using System.Threading;
using System.Collections.Generic;
using UnityEngine;
using UnityEditor.Scripting.Python;

public class tower : MonoBehaviour
{
    Thread FlaskThread = null;
    Transform[] tList = new Transform[4];
    Rigidbody[] rList = new Rigidbody[4];
    float[] vList = new float[4] { 0, 0, 0, 0 };

    // scope.Set("tower", this);
    void PythonRun(string baseDir)
    {
        Debug.Log("init PythonRun");
        PythonRunner.RunFile($"{baseDir}/Scripts/flask_op.py", "builtin", new Dictionary<string, object>() { { "vList", vList } });
        Debug.Log("exit PythonRun");
    }

    // Start is called before the first frame update
    void Start()
    {
        string dataPathTemp = Application.dataPath;
        tList[0] = this.gameObject.transform.GetChild(1);
        tList[1] = tList[0].GetChild(0);
        for (int i = 0; i != 2; ++i)
        {
            rList[i] = tList[i].gameObject.GetComponent<Rigidbody>();
        }
        PythonRunner.EnsureInitialized();
        // PythonRun(OnApplicationQuit.dataPath);
        FlaskThread = new Thread(() => PythonRun(dataPathTemp));
        FlaskThread.IsBackground = true; // to quit when foreground thread is ended
        FlaskThread.Start();
    }

    // Update is called once per frame
    void Update()
    {
        Quaternion deltaRotation = Quaternion.Euler(new Vector3(0, vList[1], 0) * Time.fixedDeltaTime);
        tList[1].Translate(Vector3.up * vList[0] * Time.fixedDeltaTime);
        tList[0].Rotate(0, vList[1] * Time.fixedDeltaTime, 0);
        tList[1].Translate(Vector3.back * vList[2] * Time.fixedDeltaTime);
        tList[0].Translate(Vector3.back * vList[3] * Time.fixedDeltaTime);
        // Debug.Log(vList[0]);Debug.Log(vList[1]);
    }

    void OnApplicationQuit()
    {
        PythonRunner.Shutdown();
        FlaskThread.Abort(); // silly method
        Debug.Log("I should abort you");
    }
}
