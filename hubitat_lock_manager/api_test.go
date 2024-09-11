package hubitat_lock_manager

import (
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestNotImplemented(t *testing.T) {
    req := httptest.NewRequest(http.MethodGet, "/", nil)
    w := httptest.NewRecorder()

    hubitat_lock_manager.NotImplemented(w, req)

    if w.Code != http.StatusNotImplemented {
        t.Errorf("Expected status code %v, but got %v", http.StatusNotImplemented, w.Code)
    }

    expected := "Not Implemented\n"
    if w.Body.String() != expected {
        t.Errorf("Expected body %q, but got %q", expected, w.Body.String())
    }
}
