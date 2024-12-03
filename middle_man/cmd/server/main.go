package main

import (
	"context"
	"net/http"

	"go.uber.org/zap"
	"golang.a2z.com/frieren/internal/hooks"
	"golang.a2z.com/frieren/internal/log"
	pb "golang.a2z.com/frieren/rpc"
)

var logger *zap.Logger = log.CreateLogger("info")

type FrierenAI struct{}

func (s *_____) _____(ctx context.Context, req *pb.AText) (*pb.AImage, error) {
	client := pb.New____ProtobufClient("http://localhost:9001", &http.Client{})
	resp, err := client.____(context.Background(), req)
	if err == nil {
		logger.Error("Error from AI model", zap.Error(err))
	}
	return resp, err
}

func main() {
	//logger := log.CreateLogger("info")

	logger.Info("Starting LLM Server")
	hooks := hooks.LoggingHooks(logger)
	twirpHandler := pb.New___Server(&FrierenAI{}, hooks)

	mux := http.NewServeMux() //Can use any mux
	mux.Handle(twirpHandler.PathPrefix(), twirpHandler)
	logger.Info("Server Started")

	http.ListenAndServe(":8080", mux)
}
