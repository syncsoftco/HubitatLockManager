package hubitat_lock_manager


import (
    "bytes"
    "fmt"
    "net/http"
    "net/http/httptest"
    "testing"
)

var executeCommand func(args ...string) (string, error)

func mockExecuteCommandSuccess(args ...string) (string, error) {
	return `{"result": "success"}`, nil
}

func mockExecuteCommandFailure(args ...string) (string, error) {
	return "", fmt.Errorf("command failed")
}

func TestCreateKeyCode(t *testing.T) {
	tests := []struct {
		name       string
		body       string
		mock       func(args ...string) (string, error)
		wantStatus int
	}{
		{
			name:       "success",
			body:       `{"code": "123456", "username": "user1", "device_id": 1}`,
			mock:       mockExecuteCommandSuccess,
			wantStatus: http.StatusOK,
		},
		{
			name:       "failure",
			body:       `{"code": "123456", "username": "user1", "device_id": 1}`,
			mock:       mockExecuteCommandFailure,
			wantStatus: http.StatusInternalServerError,
		},
		{
			name:       "invalid input",
			body:       `{"invalid_json}`,
			mock:       mockExecuteCommandSuccess,
			wantStatus: http.StatusBadRequest,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			executeCommand = tt.mock
			req := httptest.NewRequest(http.MethodPost, "/create_key_code", bytes.NewBuffer([]byte(tt.body)))
			w := httptest.NewRecorder()

			api.CreateKeyCode(w, req)

			if w.Code != tt.wantStatus {
				t.Errorf("expected status %v, got %v", tt.wantStatus, w.Code)
			}
		})
	}
}

func TestDeleteKeyCode(t *testing.T) {
	tests := []struct {
		name       string
		body       string
		mock       func(args ...string) (string, error)
		wantStatus int
	}{
		{
			name:       "success",
			body:       `{"username": "user1", "device_id": 1}`,
			mock:       mockExecuteCommandSuccess,
			wantStatus: http.StatusOK,
		},
		{
			name:       "failure",
			body:       `{"username": "user1", "device_id": 1}`,
			mock:       mockExecuteCommandFailure,
			wantStatus: http.StatusInternalServerError,
		},
		{
			name:       "invalid input",
			body:       `{"invalid_json}`,
			mock:       mockExecuteCommandSuccess,
			wantStatus: http.StatusBadRequest,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			executeCommand = tt.mock
			req := httptest.NewRequest(http.MethodDelete, "/delete_key_code", bytes.NewBuffer([]byte(tt.body)))
			w := httptest.NewRecorder()

			api.DeleteKeyCode(w, req)

			if w.Code != tt.wantStatus {
				t.Errorf("expected status %v, got %v", tt.wantStatus, w.Code)
			}
		})
	}
}

func TestListDevices(t *testing.T) {
	tests := []struct {
		name       string
		mock       func(args ...string) (string, error)
		wantStatus int
	}{
		{
			name:       "success",
			mock:       mockExecuteCommandSuccess,
			wantStatus: http.StatusOK,
		},
		{
			name:       "failure",
			mock:       mockExecuteCommandFailure,
			wantStatus: http.StatusInternalServerError,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			executeCommand = tt.mock
			req := httptest.NewRequest(http.MethodGet, "/list_devices", nil)
			w := httptest.NewRecorder()

			api.ListDevices(w, req)

			if w.Code != tt.wantStatus {
				t.Errorf("expected status %v, got %v", tt.wantStatus, w.Code)
			}
		})
	}
}

func TestListKeyCodes(t *testing.T) {
	tests := []struct {
		name       string
		query      string
		mock       func(args ...string) (string, error)
		wantStatus int
	}{
		{
			name:       "success",
			query:      "device_id=1",
			mock:       mockExecuteCommandSuccess,
			wantStatus: http.StatusOK,
		},
		{
			name:       "failure",
			query:      "device_id=1",
			mock:       mockExecuteCommandFailure,
			wantStatus: http.StatusInternalServerError,
		},
		{
			name:       "missing device_id",
			query:      "",
			mock:       mockExecuteCommandSuccess,
			wantStatus: http.StatusBadRequest,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			executeCommand = tt.mock
			req := httptest.NewRequest(http.MethodGet, "/list_key_codes?"+tt.query, nil)
			w := httptest.NewRecorder()

			api.ListKeyCodes(w, req)

			if w.Code != tt.wantStatus {
				t.Errorf("expected status %v, got %v", tt.wantStatus, w.Code)
			}
		})
	}
}
