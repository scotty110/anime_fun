package main

import (
	"bufio"
	"context"
	"fmt"
	"net/http"
	"os"

	pb "golang.a2z.com/frieren/rpc"
)

func main() {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Enter text: ")
	text, _ := reader.ReadString('\n')
	inputString := &pb.PromptText{Text: text}

	// Create a client capable of talking to server
	// Copied from twitch
	client := pb.New___ProtobufClient("http://localhost:8080", &http.Client{})
	var (
		gt  *pb.GeneratedText
		err error
	)

	gt, err = client.____(context.Background(), inputString)
	if err != nil {
		fmt.Println("Errored out")
		fmt.Println(err)
	} else {
		fmt.Println(gt)
	}
}
