# Recording Import Worker test script

End to end test script for the Recording Import Worker (RIW).

## Prerequisites

This test should be run on a machine with a running installation of the core IV software, with the recording import worker installed, configured and running. For information on installing and confguring your recording import worker instance, [please see the documentation on the RIW core worker repo.](https://github.com/IntelligentVoice/recording-import)

## Testing

1. Confirm that the recording import worker is currently installed and connected to the Gearman server:

   ```bash
   docker ps
   docker logs recording_import_worker
   ```

2. Clone this repository on your host machine:

   ```bash
   git clone git@github.com:IntelligentVoice/gearman-iv-recording-import-worker.git
   ```

3. Create and acitvate a virtual python environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

4. Install test dependencies:

   ```bash
   cd tests
   pip install requirements/python3_gmtasks-1.0-py3-none-any.whl
   ```

5. Run the test script:

   ```bash
   python test_riw.py --configure-worker
   ```

6. Check the logs of the recording import and confirm that `recording-1` was imported correctly:
   ```bash
   docker logs recording_import_worker
   ```
