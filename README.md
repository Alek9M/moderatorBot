## Telegram Group Management Bot with Firebase

This repository contains a [Telegram bot](https://core.telegram.org/bots) that was designed for a non-profit community in the UK 🇬🇧

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
- [**Moderation**](https://cloud.google.com/natural-language/docs/moderating-text): Automatically checks messages for potentially harmful content and notifies the group moderators
- **Subscriptions**: Members can subscribe or unsubscribe, receiving notifications about group activities and consenting for data collection

### Requirements
[Python 3.11](https://www.python.org/ftp/python/3.11.9/Python-3.11.9.tar.xz)

[Google Cloud CLI](https://cloud.google.com/sdk/docs/install) with [set up credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc#on-prem)

### Setup

1. **Install Dependencies**:
   ```bash
   pip3.11 install -r requirements.txt
   ```
1. **Set Environment**:
   - Insert your telegram bot [token](https://core.telegram.org/bots/tutorial#obtain-your-bot-token) by [@BotFather](https://telegram.me/BotFather)
   - Copy your [`firebase-serviceAccountKey.json`](firebase-serviceAccountKey.json.example) from https://console.firebase.google.com/project/[YOUR_PROJECT]/settings/serviceaccounts/adminsdk
   - Set a password for registering group in [`.env`](.env.example)

3. **Setup Firebase**: 
   - [Create a Firebase project](https://console.firebase.google.com)
  
### Files Overview

- `firebase.py`: Manages Firebase CRUD operations; Keeps a local copy to reduce server queries
- `main.py`: Entry point for the Telegram bot, handling commands and messages
- `moderator.py`: Contains moderation logic to identify potentially harmful messages

    
### Cost saving features
[Google Cloud Natural Language API](https://cloud.google.com/natural-language/pricing) with free 50K/month text assesment

[Firestore](https://cloud.google.com/firestore/pricing) for persistent NoSQL storage. _As none of this data is crucial - bot keeps a local copy to reduce queries_

**Runs on**

~~[Google Cloud Compute Engine](https://cloud.google.com/free/docs/free-cloud-features#compute) *non-preemptible e2-micro* in *South Carolina: us-east1*~~ 

[AWS EC2](https://aws.amazon.com/ec2/) t2.micro _free for 12 month till April '25_

*Based on average text length, population and turnover in the community it all should be within free tier. A budget alert was set*
