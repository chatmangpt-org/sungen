import typer
import requests
from typing import Optional
from pydantic import BaseModel

app = typer.Typer()

BASE_URL = "http://localhost:4000"  # Adjust this to your actual API base URL

class Ticket(BaseModel):
    id: str
    subject: str
    status: str
    representative_id: Optional[str] = None

class Representative(BaseModel):
    id: str
    name: str

@app.command()
def list_tickets():
    """List all tickets"""
    response = requests.get(f"{BASE_URL}/tickets")
    tickets = response.json()["data"]
    for ticket in tickets:
        typer.echo(f"ID: {ticket['id']}, Subject: {ticket['attributes']['subject']}, Status: {ticket['attributes']['status']}")

@app.command()
def open_ticket(subject: str):
    """Open a new ticket"""
    data = {"data": {"type": "ticket", "attributes": {"subject": subject}}}
    response = requests.post(f"{BASE_URL}/tickets", json=data)
    ticket = response.json()["data"]
    typer.echo(f"Ticket opened - ID: {ticket['id']}, Subject: {ticket['attributes']['subject']}")

@app.command()
def close_ticket(ticket_id: str):
    """Close a ticket"""
    data = {"data": {"type": "ticket", "id": ticket_id}}
    response = requests.patch(f"{BASE_URL}/tickets/{ticket_id}/close", json=data)
    if response.status_code == 200:
        typer.echo(f"Ticket {ticket_id} closed successfully")
    else:
        typer.echo(f"Failed to close ticket {ticket_id}")

@app.command()
def assign_ticket(ticket_id: str, representative_id: str):
    """Assign a ticket to a representative"""
    data = {"data": {"type": "ticket", "id": ticket_id, "attributes": {"representative_id": representative_id}}}
    response = requests.patch(f"{BASE_URL}/tickets/{ticket_id}/assign", json=data)
    if response.status_code == 200:
        typer.echo(f"Ticket {ticket_id} assigned to representative {representative_id}")
    else:
        typer.echo(f"Failed to assign ticket {ticket_id}")

@app.command()
def list_representatives():
    """List all representatives"""
    response = requests.get(f"{BASE_URL}/representatives")
    representatives = response.json()["data"]
    for rep in representatives:
        typer.echo(f"ID: {rep['id']}, Name: {rep['attributes']['name']}")

@app.command()
def add_representative(name: str):
    """Add a new representative"""
    data = {"data": {"type": "representative", "attributes": {"name": name}}}
    response = requests.post(f"{BASE_URL}/representatives", json=data)
    rep = response.json()["data"]
    typer.echo(f"Representative added - ID: {rep['id']}, Name: {rep['attributes']['name']}")


def main():
    response = requests.get(f"{BASE_URL}/tickets")
    tickets = response.json()["data"]
    for ticket in tickets:
      print(ticket)


if __name__ == "__main__":
    main()
