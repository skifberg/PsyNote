#!/bin/bash
cd backend/app
uvicorn main:app --reload --port 8001
