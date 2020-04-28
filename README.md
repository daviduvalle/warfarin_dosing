# Warfarin dosing

The project contains two baseline algorithms and one linear multi-arm bandit. (LinUCB) All try to find the right dose of Warfarin which is a treatment for blood cloths. This problem as simplification since it assigns low/med/high doses instead of actual milligrams.

# Run 
    virtualenv -p python3 myenv; source myenv/bin/activate
    pip -r requirements.txt
    # Run baselines
    python baselines.py
    # Run linucb2
    python linucb2.py


# Credits
Full credit to nickguo for his original implementation of LinUCB: (https://github.com/chuchro3/Warfarin) this implementation modifies the featurization procedure and gets extra 5% of accuracy.
