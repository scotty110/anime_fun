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

func (s *FrierenAI) GenPlayingCard(ctx context.Context, req *pb.AText) (*pb.AImage, error) {
	// Call to Create Bio
	bio_client := pb.NewGenBioServiceProtobufClient("http://localhost:9001", &http.Client{})
	bio, err := bio_client.GenBio(context.Background(), req)
	if err != nil {
		logger.Error("Error from Bio AI model", zap.Error(err))
	}

	// Call to Create Image
	image_client := pb.NewGenCharacterServiceProtobufClient("http://localhost:9002", &http.Client{})
	image, err := image_client.GenCharacter(context.Background(), bio)
	if err != nil {
		logger.Error("Error from Image AI model", zap.Error(err))
	}

	// Call to Caption Image
	caption_client := pb.NewImageCaptionServiceProtobufClient("http://localhost:9003", &http.Client{})
	card, err := caption_client.CaptionImage(context.Background(), TODO)
	if err != nil {
		logger.Error("Error from Image Caption service", zap.Error(err))
	}

	return card, err
}

func main() {
	//logger := log.CreateLogger("info")

	logger.Info("Starting AI Servers")
	hooks := hooks.LoggingHooks(logger)
	twirpHandler := pb.NewGenPlayingCardServiceServer(&FrierenAI{}, hooks)

	mux := http.NewServeMux() //Can use any mux
	mux.Handle(twirpHandler.PathPrefix(), twirpHandler)
	logger.Info("Server Started")

	http.ListenAndServe(":8080", mux)
}
