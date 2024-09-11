package hubitat_lock_manager

import (
    "net/http"
)

// NotImplemented is a placeholder function that returns a "Not Implemented" status.
func NotImplemented(w http.ResponseWriter, r *http.Request) {
    http.Error(w, "Not Implemented", http.StatusNotImplemented)
}
