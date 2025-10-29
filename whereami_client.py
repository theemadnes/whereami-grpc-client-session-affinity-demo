import grpc
import argparse
import sys
import os

# Import the generated protobuf and gRPC stub files.
# These files (whereami_pb2.py and whereami_pb2_grpc.py)
# are expected to be in the same directory as this script,
# or in a directory that's on the Python path.
# We'll assume they are generated in the current directory for simplicity.
try:
    from protos import whereami_pb2
    from protos import whereami_pb2_grpc
except ImportError:
    print("Error: Could not import generated protobuf files.", file=sys.stderr)
    print("Please ensure you have generated 'whereami_pb2.py' and 'whereami_pb2_grpc.py'.", file=sys.stderr)
    print("You can generate them using the command:", file=sys.stderr)
    print("  python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. protos/whereami.proto", file=sys.stderr)
    print("  (assuming 'protos/whereami.proto' is the correct path relative to your current directory)", file=sys.stderr)
    sys.exit(1)


def run(server_address: str):
    """
    Connects to the gRPC server at the given address and calls the GetPayload method.
    Prints the response and its individual fields.
    """
    print(f"Attempting to connect to gRPC server at: {server_address}")
    try:
        # Create an insecure channel to the gRPC server.
        # For production environments, consider using secure channels (SSL/TLS).
        with grpc.insecure_channel(server_address) as channel:
            # Create a gRPC stub for the Whereami service
            stub = whereami_pb2_grpc.WhereamiStub(channel)

            print("Calling Whereami.GetPayload()...")
            # Create an empty request message as defined in whereami.proto
            request = whereami_pb2.Empty()

            # Call the RPC method
            response = stub.GetPayload(request)

            print("\n--- gRPC Response (Full Message) ---")
            # The default __str__ representation of a protobuf message is quite readable
            print(response)

            print("\n--- gRPC Response Details (Individual Fields) ---")
            # Iterate through the fields of the WhereamiReply message and print them
            # This explicitly shows each "header" or piece of metadata returned.
            for field_descriptor, value in response.ListFields():
                # For nested messages like 'backend_result', print its string representation
                if field_descriptor.type == field_descriptor.TYPE_MESSAGE:
                    print(f"{field_descriptor.name}:")
                    # Indent nested message fields for better readability
                    # This handles the recursive 'backend_result' field gracefully.
                    if hasattr(value, 'ListFields'): # Check if it's a protobuf message
                        for nested_field_descriptor, nested_value in value.ListFields():
                            print(f"  {nested_field_descriptor.name}: {nested_value}")
                    else: # Fallback for non-protobuf message objects if any
                        print(f"  {value}")
                else:
                    print(f"{field_descriptor.name}: {value}")

    except grpc.RpcError as e:
        print(f"\n--- gRPC Error ---", file=sys.stderr)
        print(f"Status Code: {e.code()}", file=sys.stderr)
        print(f"Details: {e.details()}", file=sys.stderr)
        if e.code() == grpc.StatusCode.UNAVAILABLE:
            print("The gRPC server might not be running or is unreachable.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n--- An unexpected error occurred ---", file=sys.stderr)
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="A gRPC client for the 'Whereami' service. "
                    "Connects to a specified server and calls the GetPayload method "
                    "to retrieve backend metadata."
    )
    parser.add_argument(
        "server_address",
        type=str,
        help="The address of the gRPC server (e.g., 'localhost:50051', '127.0.0.1:8080')."
    )
    args = parser.parse_args()

    run(args.server_address)


if __name__ == "__main__":
    main()