package main

import (
	"flag"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"path/filepath"
)

var httpListen = flag.String("http-listen", ":8080", "port to listen on")

func main() {
	http.HandleFunc("/", handler)
	log.Printf("listening on http://localhost%v", *httpListen)
	http.ListenAndServe(*httpListen, nil)
}

func handler(w http.ResponseWriter, r *http.Request) {
	err := renderTemplate(w, "lookup.gohtml")
	if err != nil {
		log.Printf("internal error: %v", err)
		http.Error(w, fmt.Sprintf("%v", err), http.StatusInternalServerError)
		return
	}
}

func renderTemplate(w http.ResponseWriter, page string) error {
	lf := filepath.Join("templates", page)
	tmpl, err := template.New("tmpl").ParseFiles(lf)
	if err != nil {
		return err
	}
	return tmpl.ExecuteTemplate(w, "layout", nil)
}
