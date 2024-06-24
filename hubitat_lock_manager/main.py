from hubitat_lock_manager.batch_job import init_batch_job
from hubitat_lock_manager.api import app

if __name__ == "__main__":
    batch_job = init_batch_job(driver_path="path/to/chromedriver", hubitat_url="http://hubitat.local", username="user", password="pass", db_connection=None)
    run_batch_job(batch_job)
    app.run()
