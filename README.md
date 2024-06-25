<img src="LeaftyLogo.png" >

## Leafty - Backend
This repository contains the backend code for the Leafty project, built using Python and FastAPI as the framework.

## What is Leafty?
 Collaborative Task Management System for small and medium-sized enterprise specializing in Moringa-based products. The system will digitize and streamline the supply chain from cultivation to market, directly addressing the manual inefficiencies and information discrepancies hindering company's production planning and execution. 

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Main Folder Structure](#main-folder-structure)
- [Promo Video](#promo-video)
- [Deployment](#deployment)
- [Contributors](#contributors)

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/WADSFinalProject/Leafty-BE.git

## Usage
1. Run the development server:
    ```sh
    uvicorn main:app --reload

## Promo Video

https://drive.google.com/file/d/1QT06VqAyc-RyDzdizvv_npj0hTLOaGlk/view?usp=sharing

## Deployment
There are several things that needs to be configured before deploying in Vercel:
- `Pipfile` : A File that configures the Python version to 3.9, since some packages only supports Python 3.9 in Vercel.
- `Requirements.txt`: A File that contains packages that needs to be installed for python
- `package.json`: A File that contains which Node version needs to be used.
- `Vercel.json`: Allows the Vercel to navigate/access the endpoints for the API.

# Contributors:
- DNeilson67 - Davin Neilson (Supervisor)
- Mohammad Sulthan Azka
- Joseph Ruys
- Troy Prajoga
- Pranav


