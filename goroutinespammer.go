package main

import (
    "bufio"
    "crypto/sha256"
    "fmt"
    "net/http"
    "strings"
    "sync"
    "os"
)

func main() {
    resp, err := http.Get("https://pub-7c09b33f98f94ab5854c16d813cd1110.r2.dev/haystack.txt")
    if err != nil {
        panic(err)
    }
    defer resp.Body.Close()

    // Set the maximum number of concurrent goroutines to 1048570
    maxConcurrent := 1048570
    sem := make(chan struct{}, maxConcurrent)

    var wg sync.WaitGroup
    scanner := bufio.NewScanner(resp.Body)
    for scanner.Scan() {
        sem <- struct{}{}
        wg.Add(1)
        go func(line string) {
            defer wg.Done()
            line = strings.TrimSpace(line)
            hash := sha256.Sum256([]byte(line))
            if fmt.Sprintf("%x", hash) == "4b3adff6102a9b358da21aef582444d30fc375db798ff14dd3fb89d296819bd5" {
                fmt.Println("FOUND")
                fmt.Println(line)
                os.Exit(3)
            } else {
                fmt.Printf("Bruteforcing %s\n", line)
            }
            <-sem
        }(scanner.Text())
    }
    if err := scanner.Err(); err != nil {
        panic(err)
    }
    wg.Wait()
}
