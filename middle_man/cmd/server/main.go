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

// GenPlayingCard handles the orchestration of bio generation, image creation, and captioning
func (s *FrierenAI) GenPlayingCard(ctx context.Context, req *pb.AText) (*pb.AImage, error) {
    // Call to Create Bio
    bioClient := pb.NewGenBioServiceProtobufClient("http://localhost:9001", &http.Client{})
    bio, err := bioClient.GenBio(context.Background(), req)
    if err != nil {
        logger.Error("Error from Bio AI model", zap.Error(err))
        return nil, err
    }

    // Call to Create Image
    imageClient := pb.NewGenCharacterServiceProtobufClient("http://localhost:9002", &http.Client{})
    image, err := imageClient.GenCharacter(context.Background(), bio)
    if err != nil {
        logger.Error("Error from Image AI model", zap.Error(err))
        return nil, err
    }

    // Call to Caption Image
    captionClient := pb.NewImageCaptionServiceProtobufClient("http://localhost:9003", &http.Client{})
    card, err := captionClient.CaptionImage(context.Background(), &pb.ImageCaption{Text: bio.Text, Image: image.Image})
    if err != nil {
        logger.Error("Error from Image Caption service", zap.Error(err))
        return nil, err
    }

    return card, nil
}

func main() {
	logger.Info("Starting AI Servers")
	hooks := hooks.LoggingHooks(logger)
	twirpHandler := pb.NewGenPlayingCardServiceServer(&FrierenAI{}, hooks)
	// Other services are python implementations and started seperatly 

	mux := http.NewServeMux() //Can use any mux
	mux.Handle(twirpHandler.PathPrefix(), twirpHandler)
	logger.Info("Server Started")

	http.ListenAndServe(":8080", mux)
}
