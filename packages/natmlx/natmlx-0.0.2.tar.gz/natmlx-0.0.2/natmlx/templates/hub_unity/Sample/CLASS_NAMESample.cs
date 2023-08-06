/* 
*   NAME
*   Copyright (c) 2021 AUTHOR.
*/

namespace CLASS_NAME.Examples {

    using UnityEngine;
    using NatSuite.ML;
    using NatSuite.ML.Features;

    public sealed class CLASS_NAMESample : MonoBehaviour {
        
        [Header(@"NatML Hub")]
        public string accessKey;

        MLModelData modelData;
        MLModel model;
        CLASS_NAMEHubPredictor predictor;

        async void Start () {
            Debug.Log("Fetching model from NatML Hub");
            // Fetch model data from NatML Hub
            var modelData = await MLModelData.FromHub(
                "TAG",          // Model tag from when we created the draft on Hub
                accessKey,          // Get your access key from https://hub.natml.ai/profile
                cache: false        // Disable caching when implementing the predictor
            );
            // Deserialize the model
            var model = modelData.Deserialize();
            // Create the predictor
            var predictor = new CLASS_NAMEHubPredictor(model);

            // Make predictions
            // ...

            // Dispose the model
            model.Dispose();
        }
    }
}