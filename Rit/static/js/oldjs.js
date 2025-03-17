
import { Web3Modal } from "@web3modal/standalone";

// Initialize Web3Modal
const webmodal = new Web3Modal({
  projectId: "00b95b19b6bedb4ef761d599cc9ba0c2", // Get it from https://cloud.walletconnect.com
  walletConnectVersion: 2,
});

// Function to detect and connect to a wallet
async function connectWallet() {
  const instance = await webmodal.connect();
  const provider = new ethers.providers.Web3Provider(instance);
  console.log("Wallet connected:", provider);
}



async function addCustomChain() {
  const provider = window.ethereum; // Ensure `window.ethereum` is available

  if (!provider) {
    alert("No Ethereum-compatible wallet detected");
    return;
  }

  try {
    await provider.request({
      method: "wallet_addEthereumChain",
      params: [
        {
          chainId: "0x55A", // Chain ID in hexadecimal (e.g., 4660 is 0x1234)
          chainName: "Ramessta Network",
          rpcUrls: ["https://blockchain.ramestta.com"], // Your RPC URL
          nativeCurrency: {
            name: "RAMESTTA",
            symbol: "RAMA", // Symbol for your chain's token
            decimals: 18,
          },
          blockExplorerUrls: [" https://ramascan.com/"], // Optional block explorer URL
        },
      ],
    });

    console.log("Custom chain added successfully");
  } catch (error) {
    console.error("Failed to add custom chain:", error);
  }
}

// Combine it with wallet connection
async function connectAndAddChain() {
  await connectWallet();
  await addCustomChain();
}




async function switchToCustomChain() {
  try {
    await window.ethereum.request({
      method: "wallet_switchEthereumChain",
      params: [{ chainId: "0x55A" }], // Replace with your chain ID
    });

    console.log("Switched to custom chain");
  } catch (error) {
    if (error.code === 4902) {
      console.error("Chain not found. Adding chain...");
      await addCustomChain(); // Add the chain if not already added
    } else {
      console.error("Failed to switch chain:", error);
    }
  }
}





document.addEventListener('DOMContentLoaded', () => {
  // Get the wallet connect button by ID
  const walletConnectButton = document.getElementById('connectWalletButton');

  // Ensure the button exists and add a click event listener
  if (walletConnectButton) {
    walletConnectButton.addEventListener('click', async () => {
      try {
        // Connect wallet and ensure custom chain is added and switched
        await connectAndAddChain();
        console.log('Wallet connected and custom chain ensured.');
      } catch (error) {
        console.error('Error during wallet connection or chain setup:', error);
      }
    });
  } else {
    console.warn('Button with ID "walletconnectbtn" not found.');
  }
});
















// import { EthereumProvider } from '@walletconnect/ethereum-provider';
// import Web3 from 'web3';

// document.addEventListener('DOMContentLoaded', async () => {
//   const provider = await EthereumProvider.init({
//     projectId: "00b95b19b6bedb4ef761d599cc9ba0c2", // Replace with your WalletConnect Project ID
//     metadata: {
//       name: "ritcoin",
//       description: "ritcoin earning platform",
//       url: "https://www.ritcoin.exchange",
//       icons: ["https://avatars.githubusercontent.com/u/37784886"],
//     },
//     showQrModal: true,
//     optionalChains: [1, 56, 1370], // Add RAMESTTA chain ID
//     rpcMap: {
//       1: 'https://mainnet.infura.io/v3/3ca323afa29143b8a8d9dcbc148d915e',
//       56: "https://bsc-dataseed.binance.org/", // BSC RPC URL
//       1370: "https://blockchain.ramestta.com", // RAMESTTA RPC URL
//     },
//   });

//   const connectButton = document.getElementById('connectWalletButton');
//   const connectButtonRT = document.getElementById('connectWalletButtonRT');
//   const walletAdd = document.getElementById('walletAdd');
//   const walletAddRT = document.getElementById('walletAddRT');

//   // Utility function to fetch balances
//   const getBalances = async (web3, account, rpcUrl, usdtContractAddress = null, usdtAbi = null) => {
//     const balances = {};

//     // Native balance
//     balances.native = web3.utils.fromWei(await web3.eth.getBalance(account), 'ether');

//     // USDT balance (if applicable)
//     if (usdtContractAddress && usdtAbi) {
//       const usdtContract = new web3.eth.Contract(usdtAbi, usdtContractAddress);
//       const usdtBalance = await usdtContract.methods.balanceOf(account).call();
//       balances.usdt = web3.utils.fromWei(usdtBalance, 'ether');
//     }

//     return balances;
//   };

//   // Function to connect wallet and fetch balances
//   async function connectWallet() {
//     try {
//       await provider.enable();
//       const web3 = new Web3(provider);
//       const accounts = await web3.eth.getAccounts();
//       const account = accounts[0];
//       localStorage.setItem('connectedAccount', account);

//       // BSC balances
//       const bscWeb3 = new Web3('https://bsc-dataseed.binance.org/');
//       const usdtAbiResponse = await fetch('/member/get-usdt-abi/');
//       const usdtAbiData = await usdtAbiResponse.json();
//       if (!usdtAbiData.abi) throw new Error('Failed to retrieve USDT contract ABI');

//       const bscBalances = await getBalances(bscWeb3, account, 'https://bsc-dataseed.binance.org/', '0x55d398326f99059fF775485246999027B3197955', usdtAbiData.abi);

//       // RAMESTTA balances
//       const ramWeb3 = new Web3('https://blockchain.ramestta.com');
//       const ramBalances = await getBalances(ramWeb3, account, 'https://blockchain.ramestta.com');

//       console.log('Connected account:', account);
//       console.log('BNB Balance:', bscBalances.native, 'BNB');
//       console.log('USDT Balance:', bscBalances.usdt, 'USDT');
//       console.log('RAMESTTA Balance:', ramBalances.native, 'RAMA');

//       // Update UI
//       connectButton.innerText = `Connected: ${account}`;
//       connectButton.disabled = true;
//       connectButton.classList.add('disabled');
//       if (walletAdd) walletAdd.value = account;

//       return { web3, account, bscBalances, ramBalances };
//     } catch (error) {
//       console.error('Error connecting wallet:', error);
//     }
//   }

//   // Function to connect wallet specifically for RAMESTTA
//   async function connectWalletRT() {
//     try {
//       await provider.enable();
//       const ramWeb3 = new Web3('https://blockchain.ramestta.com');
//       const accounts = await ramWeb3.eth.getAccounts();
//       const account = accounts[0];
//       localStorage.setItem('connectedAccount', account);

//       const ramBalances = await getBalances(ramWeb3, account, 'https://blockchain.ramestta.com');

//       console.log('Connected account:', account);
//       console.log('RAMESTTA Balance:', ramBalances.native, 'RAMA');

//       // Update UI
//       connectButtonRT.innerText = `Connected: ${account}`;
//       connectButtonRT.disabled = true;
//       connectButtonRT.classList.add('disabled');
//       if (walletAddRT) walletAddRT.value = account;

//       return { web3: ramWeb3, account, ramBalances };
//     } catch (error) {
//       console.error('Error connecting wallet:', error);
//     }
//   }

//   // Event listeners for connect buttons
//   if (connectButton) connectButton.addEventListener('click', connectWallet);
//   if (connectButtonRT) connectButtonRT.addEventListener('click', connectWalletRT);
// });
