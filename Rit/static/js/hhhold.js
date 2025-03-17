

























// // WalletConnectClient.js
// import WalletConnectClient from "@walletconnect/client";
// import { ethers } from "ethers";

// // Configuration for the custom chain "Ramessta"
// // const RAMESSTA_CHAIN_ID = 1370; // Replace with your chain's ID
// // const RAMESSTA_CHAIN_DETAILS = {
// //   chainId: `0x${RAMESSTA_CHAIN_ID.toString(16)}`,
// //   chainName: "Ramessta",
// //   nativeCurrency: {
// //     name: "Ramessta Token",
// //     symbol: "RAME",
// //     decimals: 18,
// //   },
// //   rpcUrls: ["https://rpc.ramessta.example"], // Replace with your RPC URL
// //   blockExplorerUrls: ["https://explorer.ramessta.example"], // Replace with your block explorer URL
// // };
// const RAMESSTA_CHAIN_ID = 1370;
// const RAMESSTA_CHAIN_DETAILS = {
//   chainId: `0x${RAMESSTA_CHAIN_ID.toString(16)}`, // Hexadecimal representation of Chain ID
//   chainName: "Ramessta",
//   nativeCurrency: {
//     name: "Ramessta Token",
//     symbol: "RAMA",
//     decimals: 18,
//   },
//   rpcUrls: ["https://blockchain.ramestta.com"],
//   blockExplorerUrls: ["https://ramascan.com"],
// };

// export const connectWallet = async () => {
//   try {
//     const walletConnect = new WalletConnectClient({
//       bridge: "https://bridge.walletconnect.org", // Default WalletConnect bridge
//     });

//     // Create a new session if none exists
//     if (!walletConnect.connected) {
//       await walletConnect.createSession();
//     }

//     // Event listener: WalletConnect session established
//     walletConnect.on("connect", async (error, payload) => {
//       if (error) throw error;

//       const { accounts, chainId } = payload.params[0];

//       console.log("Connected accounts:", accounts, "Connected chain:", chainId);

//       // Add Ramessta chain if not already connected
//       if (parseInt(chainId, 16) !== RAMESSTA_CHAIN_ID) {
//         try {
//           await walletConnect.sendCustomRequest({
//             method: "wallet_addEthereumChain",
//             params: [RAMESSTA_CHAIN_DETAILS],
//           });
//           console.log("Ramessta chain added successfully!");
//         } catch (err) {
//           console.error("Failed to add Ramessta chain:", err);
//         }
//       } else {
//         console.log("Already connected to Ramessta chain.");
//       }
//     });

//     // Event listener: Wallet disconnected
//     walletConnect.on("disconnect", (error) => {
//       if (error) throw error;
//       console.log("Wallet disconnected");
//     });

//     // Open the WalletConnect QR Code modal for desktop or deep link for mobile
//     if (!walletConnect.connected) {
//       const uri = walletConnect.uri;
//       console.log("WalletConnect URI:", uri);

//       // Display QR Code for desktop or deep link for mobile
//       const isMobile = /Mobi|Android/i.test(navigator.userAgent);
//       if (isMobile) {
//         const deepLink = `wc:${uri}`;
//         window.location.href = deepLink;
//       } else {
//         console.log("Use a QR code library to display the WalletConnect URI for desktop.");
//       }
//     }
//   } catch (err) {
//     console.error("Connection error:", err);
//   }
// };


// // Attach click event listener to the button
// document.addEventListener("DOMContentLoaded", () => {
//   const connectButton = document.getElementById("connectWalletButton");
//   if (connectButton) {
//     connectButton.addEventListener("click", () => {
//       console.log("Connect wallet button clicked");
//       connectWallet();
//     });
//   } else {
//     console.error("Connect wallet button not found");
//   }
// });










// // // import { WagmiConfig, createClient } from "wagmi";
// // // import { mainnet } from "wagmi/chains";
// // import { WagmiProvider, createConfig, http } from "wagmi";
// // import { mainnet } from "wagmi/chains";
// // import { ConnectKitButton, ConnectKitProvider, getDefaultClient,getDefaultConfig } from "connectkit";
// // import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
// // import ReactDOM from "react-dom";
// // import React from "react";

// // // import { ConnectKitProvider, getDefaultConfig } from "connectkit";
// // // Setup Wagmi Client
// // // const wagmiClient = createClient(
// // //   getDefaultClient({
// // //     appName: "My Wallet Connect App",
// // //     chains: [mainnet],
// // //     walletConnectProjectId: "your-walletconnect-project-id", // Replace with your WalletConnect Project ID
// // //   })
// // // );



// // const wagmiClient = createConfig(
// //   getDefaultConfig({
// //     // Your dApps chains
// //     chains: [mainnet],
// //     transports: {
// //       // RPC URL for each chain
// //       [mainnet.id]: http(
// //         `https://eth-mainnet.g.alchemy.com/v2/${process.env.NEXT_PUBLIC_ALCHEMY_ID}`,
// //       ),
// //     },

// //     // Required API Keys
// //     walletConnectProjectId: process.env.NEXT_PUBLIC_WALLETCONNECT_PROJECT_ID,

// //     // Required App Info
// //     appName: "Your App Name",

// //     // Optional App Info
// //     appDescription: "Your App Description",
// //     appUrl: "https://family.co", // your app's url
// //     appIcon: "https://family.co/logo.png", // your app's icon, no bigger than 1024x1024px (max. 1MB)
// //   }),
// // );


// // const queryClient = new QueryClient();
// // // Wallet Connect Button Component
// // // const WalletButton = () => (
// // //   <WagmiConfig client={wagmiClient}>
// // //     <ConnectKitProvider>
// // //       <ConnectKitButton />
// // //     </ConnectKitProvider>
// // //   </WagmiConfig>
// // // );



// // const WalletButton = ({ children }) => {
// //   return (
// //     <WagmiProvider config={config}>
// //       <QueryClientProvider client={queryClient}>
// //         <ConnectKitProvider>{children}</ConnectKitProvider>
// //       </QueryClientProvider>
// //     </WagmiProvider>
// //   );
// // };



// // // Inject React Component into a DOM Element
// // document.addEventListener("DOMContentLoaded", () => {
// //   const container = document.getElementById("wallet-connect-button");
// //   if (container) {
// //     ReactDOM.render(<WalletButton />, container);
// //   }
// // });
