# **XRPL-Solvency - Local ring proof generation and verification environment**

This executable developed in python during the **PBWS 2023 hackathon** is the local environnement to create ring signature for XRPL solvency. 

This app allows you to generate your creditworthiness proof based on ring signatures directly in your local environment. Each time a proof is created, an SBT (Soul Bound Token) is minted and the data are stored on IPFS. 
It also allows you to verify the signatures, by retrieving them directly from our web-app.

## **What are ring-signature** 💍
Ring signatures are a type of digital signature that allows a user to sign a message on behalf of a group without revealing which specific member signed it. The signature is created using a group of possible signers, or a "ring," and any one of the members in the ring can create the signature without revealing their identity. This makes it a useful tool for maintaining privacy in various applications, such as cryptocurrencies, whistleblowing, and anonymous messaging.
In our solution we use ring signature to give you access to proof of solvency while maintaining your privacy.

## **Configuration to create your proof** 📝

1. Go on our [website](https://web-app-virid-theta.vercel.app).
2. On the generate Proof page click on download.
3. Open ring_proof.exe and pass the arguments for your signature.
4. Your done, you have minted your SBT !!!

## **Configuration to verify a proof** 📝

1. Go on our [website](https://web-app-virid-theta.vercel.app).
2. On the verify Proof page click on download.
3. Open ring_proof_verify.exe and pass the arguments for the proof you want to verify.
4. Your done, you have verify a proof !!!

## **Structure of the repository** 
This repo is divided in 4 parties : 
  - The App folder contains the code for two apps (ring_proof and ring_proof_verifier), along with two executable files that you can download to use our proof of concept. Currently, only executables are available, but we are working to release binaries for Linux and macOS users. 
  - The ring_signature folder is where there the python implementation that we use for ring signature. Most of the code come from this library [Solcrypto](https://github.com/HarryR/solcrypto). 
  - The xrpl-utils folder is where we communicate with the XRPL. So in this folder you will get the code to retrieve the data, mint the nft and derive the key from the secret key. 
  - The main.py file is where everything take a sense. In this file there is the implementation of the creation of the proof using ring-signature and then minting an nft. 

## **Start prooving solvency**

To start using the app, simply download it from our website. No additional installation or setup is required. Just follow the instructions provided in the readme to generate or verify your proofs using ring signatures. Our goal is to make the process as straightforward and user-friendly as possible, so you can focus on what matters most: securing your solvency proof while protecting your privacy.

## **More about ring signatures**
If you're interested in learning more about ring signatures, we recommend reading the following [research article](https://people.csail.mit.edu/rivest/pubs/RST01.pdf). This paper provides an in-depth introduction to ring signatures, their properties, and their applications in privacy-preserving systems.
