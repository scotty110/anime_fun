package main

import (
    "bufio"
    "context"
    "fmt"
    "io/ioutil"
    "net/http"
    "os"

	pb "golang.a2z.com/frieren/rpc"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Enter Description of a Character: ")
	text, _ := reader.ReadString('\n')
	inputString := &pb.AText{Text: text}

	// Create a client capable of talking to server
	// Copied from twitch
	client := pb.NewFrierenAIServiceProtobufClient("http://localhost:8080", &http.Client{})
	var (
		gt  *pb.AImage
		err error
	)

	gt, err = client.GenPlayingCard(context.Background(), inputString)
	if err != nil {
		fmt.Println("Errored out")
		fmt.Println(err)
	} 
	// Write to png
	if gt != nil && len(gt.Image) > 0 {
        err := ioutil.WriteFile("anime_gen.png", gt.Image, 0644)
        if err != nil {
            fmt.Println("Failed to save image to file")
            fmt.Println(err)
        } else {
            fmt.Println("Image saved as anime_gen.png")
        }
    } else {
        fmt.Println("No image data received from the server")
    }
}