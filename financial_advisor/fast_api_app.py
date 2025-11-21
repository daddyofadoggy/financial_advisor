# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""FastAPI application for Financial Advisor Agent"""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from google.adk.apps import App
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from pydantic import BaseModel

from .agent import root_agent


@asynccontextmanager
async def lifespan(app_instance: FastAPI) -> AsyncGenerator:
    """Lifespan context manager for FastAPI app."""
    # Startup
    yield
    # Shutdown


app = FastAPI(
    title="Financial Advisor API",
    description="AI-powered financial advisory agent",
    version="0.1.0",
    lifespan=lifespan,
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "financial-advisor",
            "version": os.getenv("AGENT_VERSION", "0.0.0"),
        }
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return JSONResponse(
        content={
            "message": "Financial Advisor API",
            "docs": "/docs",
            "health": "/health",
            "agent_endpoint": "/query",
        }
    )


# Create ADK App and Runner with session service
adk_app = App(name="financial_advisor", root_agent=root_agent)
session_service = InMemorySessionService()
runner = Runner(app=adk_app, session_service=session_service)


class QueryRequest(BaseModel):
    """Request model for queries."""
    query: str
    session_id: str = "default"


class QueryResponse(BaseModel):
    """Response model for queries."""
    result: str
    session_id: str


@app.post("/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    """Query the financial advisor agent."""
    try:
        # Run the agent
        result = await runner.run_async(
            user_content=request.query,
            session_id=request.session_id,
        )

        # Extract the result
        output = result.get("financial_coordinator_output", "No response")

        return QueryResponse(
            result=str(output),
            session_id=request.session_id,
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "message": "Failed to process query",
            }
        )
