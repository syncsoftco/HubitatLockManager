package hubitat_lock_manager

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "os"
    "os/exec"
    "github.com/gorilla/mux"
)

var hubIP = os.Getenv("HUB_IP")

type KeyCodeRequest struct {
	Code     string `json:"code"`
	Username string `json:"username"`
	DeviceID int    `json:"device_id,omitempty"`
}

// Execute hubitat_lock_manager CLI command
func ExecuteCommand(args ...string) (string, error) {
	cmd := exec.Command("python3", args...) // Adjust to use your hubitat_lock_manager CLI command
	output, err := cmd.CombinedOutput()
	return string(output), err
}

// CreateKeyCode creates a new key code
func CreateKeyCode(w http.ResponseWriter, r *http.Request) {
	var req KeyCodeRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid input", http.StatusBadRequest)
		return
	}

	args := []string{"-m", "hubitat_lock_manager.main", "--hub-ip", hubIP, "--action", "create", "--username", req.Username, "--code", req.Code}
	if req.DeviceID != 0 {
		args = append(args, "--device-id", fmt.Sprint(req.DeviceID))
	}

	output, err := ExecuteCommand(args...)
	if err != nil {
		http.Error(w, output, http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(output))
}

// DeleteKeyCode deletes a key code
func DeleteKeyCode(w http.ResponseWriter, r *http.Request) {
	var req KeyCodeRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid input", http.StatusBadRequest)
		return
	}

	args := []string{"-m", "hubitat_lock_manager.main", "--hub-ip", hubIP, "--action", "delete", "--username", req.Username}
	if req.DeviceID != 0 {
		args = append(args, "--device-id", fmt.Sprint(req.DeviceID))
	}

	output, err := ExecuteCommand(args...)
	if err != nil {
		http.Error(w, output, http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(output))
}

// ListDevices lists all devices
func ListDevices(w http.ResponseWriter, r *http.Request) {
	args := []string{"-m", "hubitat_lock_manager.main", "--hub-ip", hubIP, "--action", "list_devices"}

	output, err := ExecuteCommand(args...)
	if err != nil {
		http.Error(w, output, http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(output))
}

// ListKeyCodes lists key codes for a specific device
func ListKeyCodes(w http.ResponseWriter, r *http.Request) {
	deviceID := r.URL.Query().Get("device_id")
	if deviceID == "" {
		http.Error(w, "device_id is required", http.StatusBadRequest)
		return
	}

	args := []string{"-m", "hubitat_lock_manager.main", "--hub-ip", hubIP, "--action", "list", "--device-id", deviceID}

	output, err := ExecuteCommand(args...)
	if err != nil {
		http.Error(w, output, http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(output))
}

func main() {
	r := mux.NewRouter()

	// Define routes
	r.HandleFunc("/create_key_code", CreateKeyCode).Methods("POST")
	r.HandleFunc("/delete_key_code", DeleteKeyCode).Methods("DELETE")
	r.HandleFunc("/list_devices", ListDevices).Methods("GET")
	r.HandleFunc("/list_key_codes", ListKeyCodes).Methods("GET")

	// Start the server
	log.Println("Starting server on port 5000...")
	log.Fatal(http.ListenAndServe(":5000", r))
}
