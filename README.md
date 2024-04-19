## Telegram Group Management Bot with Firebase

This repository contains a [Telegram bot](https://core.telegram.org/bots) that was designed for an online non-profit community in UK 🇬🇧

#### Issues
A dicision was made to close topic-free chat due to inability to always keep toxic messages at bay. That limits socialisation of physically isolated community members.
- Potentially problematic members
- Not enough resources
  
#### Goals
- [x] Keep a list of all members for later cross-referencing
- [x] Gather statistics on usage with minimal personal data
- [x] Identify potentially problematic messages and request human moderation
- [x] Use only free stack
- [ ] Anonymous surveys with public registery

### Features

- **Group Management**: Sets group moderation, member registery and gathers statistics
- **Moderation**: Automatically checks messages for potentially harmful content and notifies the group moderators
- **Subscriptions**: Members can subscribe or unsubscribe, receiving notifications about group activities and consenting for data collection

### Commands
#### Roles
Admin - [Telegram](https://telegram.org) account that can change bot settings in the group

#### In Groups
| Command      |    Description     |
| :----------- | :----- |
| /start [PASSWORD] | A person sending this with the correct password logs the group on Firebase and is assigned as admin |
| /notify [str: "@* @*..."]        | Set moderators to notify on raised moderation issue         |

#### In Private  
| Command      |    Description          |
| :----------- | :------------ |
| /start | Reading and signing GDPR compliant meta data collection and notifications |
| /subscribe         | Signing up for data collection and notifications         |
| /unsubscribe         | Revoking consent for historic metadata collection and deletion of it        |


### Requirements
Python 3.11

### Setup

1. **Install Dependencies**:
   ```bash
   pip3.11 install -r requirements.txt
   ```
1. **Set Environment**:
   - Insert your telegram bot [token](https://core.telegram.org/bots/tutorial#obtain-your-bot-token) by [@BotFather](https://telegram.me/BotFather)
   - Copy your `firebase-serviceAccountKey.json` from https://console.firebase.google.com/project/[YOUR_PROJECT]/settings/serviceaccounts/adminsdk
   - Set a password for registering group

3. **Setup Firebase**: 
   - [Create a Firebase project](https://console.firebase.google.com)
  
### Files Overview

- `firebase.py`: Manages Firebase CRUD operations; Keeps a local copy to reduce server queries
- `main.py`: Entry point for the Telegram bot, handling commands and messages
- `moderator.py`: Contains moderation logic to identify potentially harmful messages

    
### Cost saving features
[Google Cloud Natural Language API](https://cloud.google.com/natural-language/pricing) with free 50K/month text assesment

[Firestore](https://cloud.google.com/firestore/pricing) for persistent NoSQL storage. As none of this data is crucial - bot keeps a local copy to reduce queries

Runs on [Google Cloud Compute Engine](https://cloud.google.com/free/docs/free-cloud-features#compute) *non-preemptible e2-micro* in *South Carolina: us-east1*

*Based on average text length, population and turnover in the community it all should be within free tier. A budget alert was set*
