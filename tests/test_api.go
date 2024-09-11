package main

import (
	"bytes"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestCreateKeyCode(t *testing.T) {
	reqBody := `{"code": "123456", "username": "user1", "device_id": 1}`
	req := httptest.NewRequest(http.MethodPost, "/create_key_code", bytes.NewBuffer([]byte(reqBody)))
	w := httptest.NewRecorder()

	createKeyCode(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("expected status %v, got %v", http.StatusOK, w.Code)
	}
}

func TestListDevices(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/list_devices", nil)
	w := httptest.NewRecorder()

	listDevices(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("expected status %v, got %v", http.StatusOK, w.Code)
	}
}
