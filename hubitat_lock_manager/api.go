package main

import (
    "encoding/json"
    "fmt"
    "log"
    "net/http"
    "os"
    "os/exec"
    "sync"

    "github.com/gorilla/mux"
    "tailscale.com/tsnet"
)

var (
    hubIP          = os.Getenv("HUB_IP")
    executeCommand = ExecuteCommand // Default to the real implementation
    tsServer       *tsnet.Server
    tsOnce         sync.Once
)

type KeyCodeRequest struct {
    Code     string `json:"code"`
    Username string `json:"username"`
    DeviceID int    `json:"device_id,omitempty"`
}

// InitializeTailscale sets up tsnet and logs into the Tailnet
func InitializeTailscale() (*tsnet.Server, error) {
    tsOnce.Do(func() {
        tsServer = &tsnet.Server{
            AuthKey: os.Getenv("TS_AUTHKEY"), // Use TS_AUTHKEY for Tailscale auth
        }

        log.Printf("Starting Tailscale...")
        if _, err := tsServer.Up(); err != nil {
            log.Fatalf("Tailscale startup failed: %v", err)
        }

        log.Printf("Tailscale started successfully")
    })

    return tsServer, nil
}

// ExecuteCommand executes hubitat_lock_manager CLI command
func ExecuteCommand(args ...string) (string, error) {
    log.Printf("Executing command: python3 %v", args)
    cmd := exec.Command("python3", args...) // Adjust to use your hubitat_lock_manager CLI command
    output, err := cmd.CombinedOutput()
    log.Printf("Command output: %s", output)
    if err != nil {
        log.Printf("Error executing command: %v", err)
    }
    return string(output), err
}

// CreateKeyCode creates a new key code
func CreateKeyCode(w http.ResponseWriter, r *http.Request) {
    var req KeyCodeRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        log.Printf("Error decoding request body: %v", err)
        http.Error(w, "Invalid input", http.StatusBadRequest)
        return
    }

    args := []string{"-m", "hubitat_lock_manager.cli", "--hub-ip", hubIP, "--action", "create", "--username", req.Username, "--code", req.Code}
    if req.DeviceID != 0 {
        args = append(args, "--device-id", fmt.Sprint(req.DeviceID))
    }

    output, err := executeCommand(args...)
    if err != nil {
        log.Printf("Error creating key code: %v, Output: %s", err, output)
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
        log.Printf("Error decoding request body: %v", err)
        http.Error(w, "Invalid input", http.StatusBadRequest)
        return
    }

    args := []string{"-m", "hubitat_lock_manager.cli", "--hub-ip", hubIP, "--action", "delete", "--username", req.Username}
    if req.DeviceID != 0 {
        args = append(args, "--device-id", fmt.Sprint(req.DeviceID))
    }

    output, err := executeCommand(args...)
    if err != nil {
        log.Printf("Error deleting key code: %v, Output: %s", err, output)
        http.Error(w, output, http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    w.Write([]byte(output))
}

// ListDevices lists all devices
func ListDevices(w http.ResponseWriter, r *http.Request) {
    args := []string{"-m", "hubitat_lock_manager.cli", "--hub-ip", hubIP, "--action", "list_devices"}

    output, err := executeCommand(args...)
    if err != nil {
        log.Printf("Error listing devices: %v, Output: %s", err, output)
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
        log.Printf("Missing device_id in query")
        http.Error(w, "device_id is required", http.StatusBadRequest)
        return
    }

    args := []string{"-m", "hubitat_lock_manager.cli", "--hub-ip", hubIP, "--action", "list", "--device-id", deviceID}

    output, err := executeCommand(args...)
    if err != nil {
        log.Printf("Error listing key codes: %v, Output: %s", err, output)
        http.Error(w, output, http.StatusInternalServerError)
        return
    }

    w.Header().Set("Content-Type", "application/json")
    w.Write([]byte(output))
}

func main() {
    // Initialize Tailscale
    _, err := InitializeTailscale()
    if err != nil {
        log.Fatalf("Failed to initialize Tailscale: %v", err)
    }

    r := mux.NewRouter()

    // Define routes
    r.HandleFunc("/create_key_code", CreateKeyCode).Methods("POST")
    r.HandleFunc("/delete_key_code", DeleteKeyCode).Methods("DELETE")
    r.HandleFunc("/list_devices", ListDevices).Methods("GET")
    r.HandleFunc("/list_key_codes", ListKeyCodes).Methods("GET")

    // Get the port from the environment variable or use 5000 as the default
    port := os.Getenv("PORT")
    if port == "" {
        port = "5000"
    }

    // Start the server
    log.Printf("Starting server on port %s...\n", port)
    log.Fatal(http.ListenAndServe(":"+port, r))
}
