package helpspotgo

import (
	"context"
	"fmt"
)

func ExampleClient() {
	ctx := context.Background()

	client, err := NewClient(
		WithBaseURL("https://your-helpspot-domain.com"),
		WithAPIKey("your-api-key"),
		WithDebug(true),
	)
	if err != nil {
		fmt.Printf("Error creating client: %v\n", err)
		return
	}

	version, err := client.GetVersion(ctx)
	if err != nil {
		fmt.Printf("Error getting version: %v\n", err)
		return
	}
	fmt.Printf("API Version: %s\n", version.Version)
}
