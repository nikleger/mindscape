package infrastructure

import (
	"testing"

	"github.com/gruntwork-io/terratest/modules/terraform"
	"github.com/stretchr/testify/assert"
)

func TestTerraformInfrastructure(t *testing.T) {
	t.Parallel()

	terraformOptions := &terraform.Options{
		TerraformDir: "../../infrastructure",
		Vars: map[string]interface{}{
			"environment": "test",
		},
	}

	defer terraform.Destroy(t, terraformOptions)
	terraform.InitAndApply(t, terraformOptions)

	// Test outputs
	apiEndpoint := terraform.Output(t, terraformOptions, "api_endpoint")
	assert.NotEmpty(t, apiEndpoint)

	// Test resource creation
	instanceCount := terraform.Output(t, terraformOptions, "instance_count")
	assert.Equal(t, "3", instanceCount)
} 