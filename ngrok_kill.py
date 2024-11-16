from pyngrok import ngrok

# List all running tunnels
tunnels = ngrok.get_tunnels()
print("Running tunnels:")
for tunnel in tunnels:
    print(f"- {tunnel.public_url} -> {tunnel.config['addr']}")

# Kill all tunnels
ngrok.kill()
print("\nAll ngrok tunnels killed!")