import { EthereumProvider } from '@walletconnect/ethereum-provider';
import Web3 from 'web3';

document.addEventListener('DOMContentLoaded', async () => {



  const provider = await EthereumProvider.init({
    projectId: "00b95b19b6bedb4ef761d599cc9ba0c2", // Replace with your WalletConnect Project ID
    metadata: {
      name: "ritcoin",
      description: "ritcoin earning platform",
      url: "https://www.ritcoin.exchange",
      icons: ["https://avatars.githubusercontent.com/u/37784886"],
    },
    showQrModal: true,
    optionalChains: [1,56], // List of natively supported chains
    rpcMap: {
      1: 'https://mainnet.infura.io/v3/3ca323afa29143b8a8d9dcbc148d915e',
      56: "https://bsc-dataseed.binance.org/", // Ramestta RPC URL
    },
   
  });







  
    const connectButton = document.getElementById('connectWalletButton');
    const connectButtonRT = document.getElementById('connectWalletButtonRT');
    const walletAdd = document.getElementById('walletAdd');
    const walletAddRT = document.getElementById('walletAddRT');
    const payButton = document.getElementById('pay-button');
  
    // Function to connect wallet
    async function connectWallet() {
      try {
        await provider.enable();
        const web3 = new Web3(provider);
        const accounts = await web3.eth.getAccounts();
        const account = accounts[0];
        localStorage.setItem('connectedAccount', account);
  
        // Initialize separate Web3 instances for BSC and Ramestta
        const bscWeb3 = new Web3('https://bsc-dataseed.binance.org/');
        // const ramWeb3 = new Web3('https://blockchain.ramestta.com/');
  
        // Fetch balances from BSC
        const bnbBalance = await bscWeb3.eth.getBalance(account);
        const bnbBalanceInEth = bscWeb3.utils.fromWei(bnbBalance, 'ether');
  
        // Fetch USDT balance from BSC
        const usdtContractAddress = '0x55d398326f99059fF775485246999027B3197955'; // USDT on BSC
        const usdtABIResponse = await fetch('/member/get-usdt-abi/');
        const usdtABIData = await usdtABIResponse.json();
        if (!usdtABIData.abi) {
          throw new Error('Failed to retrieve USDT contract ABI');
        }
        const usdtContract = new bscWeb3.eth.Contract(usdtABIData.abi, usdtContractAddress);
        const usdtBalance = await usdtContract.methods.balanceOf(account).call();
        const usdtBalanceInEth = bscWeb3.utils.fromWei(usdtBalance, 'ether');
  
        // Fetch balance from Ramestta
        // const ramBalance = await ramWeb3.eth.getBalance(account);
        // const ramBalanceInEth = ramWeb3.utils.fromWei(ramBalance, 'ether');
  
        console.log('Connected account:', account);
        console.log('BNB Balance:', bnbBalanceInEth, 'BNB');
        console.log('USDT Balance:', usdtBalanceInEth, 'USDT');
        // console.log('Ramestta Balance:', ramBalanceInEth, 'RAM');
  
        // Update UI
        connectButton.innerText = `Connected: ${account}`;
        connectButton.disabled = true;
        connectButton.classList.add('disabled');
  
        if (walletAdd) {
          walletAdd.value = `${account}`;
        }
  
        return { web3, account, bnbBalanceInEth, usdtBalanceInEth };
      } catch (error) {
        console.error('Error connecting wallet:', error);
      }
    }
  
    // Function to connect wallet
    async function connectWalletRT() {
      try {
        await provider.enable();
        const web3 = new Web3(provider);
        const accounts = await web3.eth.getAccounts();
        const account = accounts[0];
        localStorage.setItem('connectedAccount', account);
  
        // Initialize separate Web3 instances for BSC and Ramestta
        // const bscWeb3 = new Web3('https://bsc-dataseed.binance.org/');
        // // const ramWeb3 = new Web3('https://blockchain.ramestta.com/');
  
        // // Fetch balances from BSC
        // const bnbBalance = await bscWeb3.eth.getBalance(account);
        // const bnbBalanceInEth = bscWeb3.utils.fromWei(bnbBalance, 'ether');
  
        // Fetch USDT balance from BSC
        // const usdtContractAddress = '0x55d398326f99059fF775485246999027B3197955'; // USDT on BSC
        // const usdtABIResponse = await fetch('/member/get-usdt-abi/');
        // const usdtABIData = await usdtABIResponse.json();
        // if (!usdtABIData.abi) {
        //   throw new Error('Failed to retrieve USDT contract ABI');
        // }
        // const usdtContract = new bscWeb3.eth.Contract(usdtABIData.abi, usdtContractAddress);
        // const usdtBalance = await usdtContract.methods.balanceOf(account).call();
        // const usdtBalanceInEth = bscWeb3.utils.fromWei(usdtBalance, 'ether');
  
        // Fetch balance from Ramestta
        // const ramBalance = await ramWeb3.eth.getBalance(account);
        // const ramBalanceInEth = ramWeb3.utils.fromWei(ramBalance, 'ether');
  
        // console.log('Connected account:', account);
        // console.log('BNB Balance:', bnbBalanceInEth, 'BNB');
        // console.log('USDT Balance:', usdtBalanceInEth, 'USDT');
        // console.log('Ramestta Balance:', ramBalanceInEth, 'RAM');
  
        // Update UI
        connectButton.innerText = `Connected: ${account}`;
        connectButton.disabled = true;
        connectButton.classList.add('disabled');
  
        if (walletAdd) {
          walletAddRT.value = `${account}`;
        }
  
        return { web3, account, bnbBalanceInEth, usdtBalanceInEth };
      } catch (error) {
        console.error('Error connecting wallet:', error);
      }
    }
  
  //   connectButton.addEventListener('click', connectWallet);
  // });
  




  async function sendTransactionHashToDjango(transactionHash, tranTimeCoinValue, coinName, cryptoAmount, amount) {
    try {
      const response = await fetch('/member/verify-transaction/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken':  `{{csrf_token}}` // Ensure csrftoken is passed correctly
        },
        body: JSON.stringify({ transactionHash, tranTimeCoinValue, coinName, cryptoAmount, amount })
      });
      const data = await response.json();
      if (data.success) {
        alert('Transaction verified and funds added to your wallet.');
        location.reload(); // Reload the page
      } else {
        alert('Transaction verification failed.');
        location.reload();
      }
    } catch (error) {
      console.error('Error sending transaction hash to Django:', error);
    }
  }
    
  const storedAccount = localStorage.getItem('connectedAccount');
  if (storedAccount) {
    await reconnectWallet(storedAccount); // Reconnect if wallet is already connected
  }

  // Function to check if wallet is already connected
  // async function checkWalletConnection() {
  //   const connectedAccount = localStorage.getItem('connectedAccount');
  //   if (connectedAccount) {
  //     console.log('Account already connected:', connectedAccount);
  //     connectButton.innerText = `Connected: ${connectedAccount}`;
  //     connectButton.disabled = true;
  //     connectButton.classList.add('disabled');

  //     if (walletAdd) {
  //       walletAdd.value = connectedAccount;
  //     }
  //   } else {
  //     console.log('No connected account found.');
  //   }
  // }


  async function payWithWallet() {


    try {
      const response = await fetch(`/member/get-busd-price/`);
      const data = await response.json();
      const priceInUsd = data.price;
      const amnt = document.getElementById('amount').value;

      if (!amnt || parseFloat(amnt) < 0) {
        alert('Invalid amount');
        location.reload();
        return;
      }

      const { web3, account,usdtContract,usdtBalance,usdtBalanceInEth } = await connectWallet();
      // const cryptoAmount = (amnt / priceInUsd).toFixed(18);
      const usdtAmount = web3.utils.toWei((amnt / priceInUsd).toFixed(18), 'ether');
      console.log('balance in eth is',usdtBalanceInEth);
      console.log('balance in usdt eth is is',amnt);

      
      // if (parseFloat(usdtBalanceInEth) < parseFloat(usdtAmount)) {
      if (parseFloat(usdtBalanceInEth) < parseFloat(amnt)) {
        alert(`Insufficient USDT balance. You need at least ${usdtBalanceInEth} USDT in your wallet to proceed.`);
        return;
    }

    // console.log('came to send transaction');

    // const txData = usdtContract.methods.transfer('0xd8956286e0A26E42ed5d3BD02D802B38B711D8aB', usdtAmount).encodeABI();
    const txData = usdtContract.methods.transfer('0x83c2cc4E02b329710c5b39f5AF2c5A5922c16756', usdtAmount).encodeABI();
    const nonce = await web3.eth.getTransactionCount(account, 'latest');
    const gasPrice = await web3.eth.getGasPrice();

    const gasLimit = await web3.eth.estimateGas({
      from: account,
      to: usdtContract.options.address,
      data: txData
  });

  // console.log('nonce is ',nonce);
  // console.log('gasprice is ',gasPrice);
  // console.log(priceInUsd, 'USDT', usdtAmount, amnt);


  // return

  console.log('gas limit is',gasLimit);
    const gasCost = web3.utils.fromWei((gasLimit * gasPrice).toString(), 'ether');

    // Check if the user has enough BNB to cover gas fees
    const bnbBalance = await web3.eth.getBalance(account);
    const bnbBalanceInEth = web3.utils.fromWei(bnbBalance, 'ether');

    if (parseFloat(bnbBalanceInEth) < parseFloat(gasCost)) {
      alert(`Insufficient BNB balance to cover gas fees. You need at least ${gasCost} BNB.`);
      return;
    }


    const tx={
      from: account,
      to: usdtContract.options.address,
      data: txData,
      gas:gasLimit,
      gasPrice: gasPrice, // Adjust the gas price as needed or use web3.eth.generateGasPrice()
      nonce: nonce,
      chainId: 56 //
    }

    web3.eth.sendTransaction(tx) .on('transactionHash', function(hash) 
      {
        console.log('Transaction Hash:', hash);
        sendTransactionHashToDjango(hash, priceInUsd, 'USDT', usdtAmount, amnt);
    
    
      })
    .on('error', console.error);
    
    // usdtContract.methods.transfer('0xd8956286e0A26E42ed5d3BD02D802B38B711D8aB', usdtAmount).send({ from: account })
    //         .on('transactionHash', function(hash) {
    //             console.log('Transaction Hash:', hash);
    //             sendTransactionHashToDjango(hash, priceInUsd, 'USDT', usdtAmount, amnt);
    //         })
    //         .on('error', console.error);



      

   

    } catch (error) {
      console.error('Error in payment process:', error);
    }
  }



  async function getUSDTBalance(web3, account) {
    const bscWeb3 = new Web3('https://bsc-dataseed.binance.org/');
    const usdtContractAddress = '0x55d398326f99059fF775485246999027B3197955'; // USDT contract address on BSC
    const response = await fetch('/member/get-usdt-abi/');
    const data = await response.json();
    if (!data.abi) {
      throw new Error('Failed to retrieve USDT contract ABI');
    }
    const usdtABI = data.abi;
    const usdtContract = new bscWeb3.eth.Contract(usdtABI, usdtContractAddress);
    const usdtBalance = await usdtContract.methods.balanceOf(account).call();
    const usdtBalanceInEth = web3.utils.fromWei(usdtBalance, 'ether');
    return usdtBalanceInEth;
  }

  async function reconnectWallet(storedAccount) {
  try {
    if (!provider.connected) {
      await provider.enable();
    }
    const web3 = new Web3(provider);
    const usdtBalanceInEth = await getUSDTBalance(web3, storedAccount);

    connectButton.innerText = `Connected: ${usdtBalanceInEth} USDT`;
    connectButton.disabled = true;
    connectButton.classList.add('disabled');

    if (walletAdd) {
      walletAdd.value = storedAccount;
    }
  } catch (error) {
    console.error('Error reconnecting wallet:', error);
    localStorage.removeItem('connectedAccount');
  }
}


  connectButton.addEventListener('click', connectWallet);
  connectButtonRT.addEventListener('click', connectWalletRT);
  payButton.addEventListener('click', payWithWallet);
});
