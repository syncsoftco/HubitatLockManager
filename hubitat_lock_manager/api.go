package main

import (
	"bytes"
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
func executeCommand(args ...string) (string, error) {
	cmd := exec.Command("python3", args...) // Adjust to use your hubitat_lock_manager CLI command
	output, err := cmd.CombinedOutput()
	return string(output), err
}

// Create key code
func createKeyCode(w http.ResponseWriter, r *http.Request) {
	var req KeyCodeRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid input", http.StatusBadRequest)
		return
	}

	args := []string{"-m", "hubitat_lock_manager.main", "--hub-ip", hubIP, "--action", "create", "--username", req.Username, "--code", req.Code}
	if req.DeviceID != 0 {
		args = append(args, "--device-id", fmt.Sprint(req.DeviceID))
	}

	output, err := executeCommand(args...)
	if err != nil {
		http.Error(w, output, http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(output))
}

// Delete key code
func deleteKeyCode(w http.ResponseWriter, r *http.Request) {
	var req KeyCodeRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid input", http.StatusBadRequest)
		return
	}

	args := []string{"-m", "hubitat_lock_manager.main", "--hub-ip", hubIP, "--action", "delete", "--username", req.Username}
	if req.DeviceID != 0 {
		args = append(args, "--device-id", fmt.Sprint(req.DeviceID))
	}

	output, err := executeCommand(args...)
	if err != nil {
		http.Error(w, output, http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(output))
}

// List devices
func listDevices(w http.ResponseWriter, r *http.Request) {
	args := []string{"-m", "hubitat_lock_manager.main", "--hub-ip", hubIP, "--action", "list_devices"}

	output, err := executeCommand(args...)
	if err != nil {
		http.Error(w, output, http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(output))
}

// List key codes
func listKeyCodes(w http.ResponseWriter, r *http.Request) {
	deviceID := r.URL.Query().Get("device_id")
	if deviceID == "" {
		http.Error(w, "device_id is required", http.StatusBadRequest)
		return
	}

	args := []string{"-m", "hubitat_lock_manager.main", "--hub-ip", hubIP, "--action", "list", "--device-id", deviceID}

	output, err := executeCommand(args...)
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
	r.HandleFunc("/create_key_code", createKeyCode).Methods("POST")
	r.HandleFunc("/delete_key_code", deleteKeyCode).Methods("DELETE")
	r.HandleFunc("/list_devices", listDevices).Methods("GET")
	r.HandleFunc("/list_key_codes", listKeyCodes).Methods("GET")

	// Start the server
	log.Println("Starting server on port 5000...")
	log.Fatal(http.ListenAndServe(":5000", r))
}
