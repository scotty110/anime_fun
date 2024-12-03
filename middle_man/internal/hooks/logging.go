package hooks

import (
	"context"

	//"fmt"
	"time"

	"github.com/twitchtv/twirp"
	"go.uber.org/zap"
	//"golang.a2z.com/frieren/cmd/server/main"
)

// https://github.com/bakins/twirpzap/blob/master/logger.go

var ctxKey = new(int)

// LoggingHooks creates a new twirp.ServerHooks which logs requests as they are
// routed to Twirp, and logs responses (including response time) when they are
// sent.
//
// This is a demonstration showing how you can use context accessors with hooks.
func LoggingHooks(logger *zap.Logger) *twirp.ServerHooks {
	//func LoggingHooks(w io.Writer) *twirp.ServerHooks {
	return &twirp.ServerHooks{
		RequestReceived: func(ctx context.Context) (context.Context, error) {
			startTime := time.Now()
			ctx = context.WithValue(ctx, ctxKey, startTime)
			return ctx, nil
		},
		RequestRouted: func(ctx context.Context) (context.Context, error) {
			svc, _ := twirp.ServiceName(ctx)
			meth, _ := twirp.MethodName(ctx)
			//fmt.Fprintf(w, "received req svc=%q method=%q\n", svc, meth)
			logger.Info("received req",
				zap.String("svc", svc),
				zap.String("method", meth),
			)
			return ctx, nil
		},
		ResponseSent: func(ctx context.Context) {
			startTime := ctx.Value(ctxKey).(time.Time)
			svc, _ := twirp.ServiceName(ctx)
			meth, _ := twirp.MethodName(ctx)
			//fmt.Fprintf(w, "response sent svc=%q method=%q time=%q\n", svc, meth, time.Since(startTime))
			logger.Info("response sent",
				zap.String("svc", svc),
				zap.String("method", meth),
				zap.Duration("time", time.Since(startTime)),
			)
		},
	}
}
