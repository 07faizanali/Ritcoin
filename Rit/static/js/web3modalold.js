// static/js/walletconnect.js

import { EthereumProvider } from '@walletconnect/ethereum-provider';
import Web3 from 'web3';

document.addEventListener('DOMContentLoaded', async () => {
  const provider = await EthereumProvider.init({
    projectId: '7490272862d63236aa7a92d593202d5e',
    metadata: {
      name: 'Ritcoin',
      description: 'Ritcoin crypto earning platform',
      url: 'https://www.ritcoin.exchange', // origin must match your domain & subdomain
      icons: ['https://avatars.githubusercontent.com/u/37784886']
    },
    showQrModal: true,
    optionalChains: [1,56, 137, 2020],
    rpcMap: {
      1: 'https://mainnet.infura.io/v3/3ca323afa29143b8a8d9dcbc148d915e',
      56: 'https://bsc-dataseed.binance.org/',
      137: 'https://polygon-rpc.com'
    }
  });

  const connectButton = document.getElementById('connectWalletButton');
  const payButton = document.getElementById('pay-button');

  
 connectButton.addEventListener('click', async () => {
    try {
      await provider.enable();
      console.log('Wallet connected');

      const web3 = new Web3(provider);
      const accounts = await web3.eth.getAccounts();
      const account = accounts[0];

      const ethBalance = await web3.eth.getBalance(account);
      // ethBalanceDisplay.textContent = `ETH Balance: ${web3.utils.fromWei(ethBalance, 'ether')} ETH`;

      const bscWeb3 = new Web3('https://bsc-dataseed.binance.org/');
      const bnbBalance = await bscWeb3.eth.getBalance(account);
      // bnbBalanceDisplay.textContent = `BNB Balance: ${bscWeb3.utils.fromWei(bnbBalance, 'ether')} BNB`;
      const usdtContractAddress = '0x55d398326f99059fF775485246999027B3197955'; // USDT contract address on BSC
      const usdtABI = [
        // Only the `balanceOf` method is needed
        {
          constant: true,
          inputs: [{ name: "_owner", type: "address" }],
          name: "balanceOf",
          outputs: [{ name: "balance", type: "uint256" }],
          type: "function"
        }
      ];

      const usdtContract = new bscWeb3.eth.Contract(usdtABI, usdtContractAddress);
      const usdtBalance = await usdtContract.methods.balanceOf(account).call();
      const usdtBalanceInEth = bscWeb3.utils.fromWei(usdtBalance, 'ether');

      // addressDisplay.textContent = `Address: ${account}`;
      connectButton.disabled = true;
      // connectButton.textContent = `Balance: ${bscWeb3.utils.fromWei(bnbBalance, 'ether')} BNB`;
      connectButton.textContent = `Balance: ${usdtBalanceInEth} USDT`;
      // const balance = await web3.eth.getBalance(account);

      // addressDisplay.textContent = `Address: ${account}`;
      // balanceDisplay.textContent = `Balance: ${web3.utils.fromWei(balance, 'ether')} ETH`;
    } catch (error) {
      console.error('Error connecting wallet:', error);
    }
  });

payButton.addEventListener('click', payWithMetaMask);



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
    

  async function payWithMetaMask() {
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
  
      const cryptoAmount = parseFloat(amnt / priceInUsd).toFixed(18);
      const web3 = new Web3(provider);
      const accounts = await web3.eth.getAccounts();
      const account = accounts[0];

      const bscWeb3 = new Web3('https://bsc-dataseed.binance.org/');
      const bnbBalance = await bscWeb3.eth.getBalance(account);
      const bnbBalanceInEth = bscWeb3.utils.fromWei(bnbBalance, 'ether');

      console.log('came to estimate gas limit:');
       // Estimate gas limit
      const gasLimit = await bscWeb3.eth.estimateGas({
        from: account,
        to: '0x83c2cc4E02b329710c5b39f5AF2c5A5922c16756',
        // value: web3.utils.toWei(cryptoAmount, 'ether')
        value: bscWeb3.utils.toWei(cryptoAmount, 'ether')
      });
      // const gasLimit = await web3.eth.estimateGas({
      //   from: account,
      //   to: '0xd8956286e0A26E42ed5d3BD02D802B38B711D8aB',
      //   // value: web3.utils.toWei(cryptoAmount, 'ether')
      //   value: bscWeb3.utils.toWei(cryptoAmount, 'ether')
      // });
      console.log('came to check gas price:');

      const gasPrice = await web3.eth.getGasPrice();
      console.log('gas price is:', gasPrice);
      const gasPriceInEth = web3.utils.fromWei(gasPrice, 'ether');
      console.log('gas price in eth is gasPriceInEth :', gasPrice);
      console.log('bnb balance in eth is  :',bnbBalanceInEth);
      console.log('gas limit is   :',gasLimit);
      const transactionCostInEth = gasPriceInEth * gasLimit;

      console.log('Transaction Cost in eth:', transactionCostInEth);
      // const transactionCost = gasPrice * gasLimit;
      // console.log('Transaction Cost:', transactionCost);

      // if (parseFloat(bnbBalanceInEth) < parseFloat(cryptoAmount)) {
      //   alert(`Insufficient BNB balance. You need at least  BNB to proceed.`);
      //   return;
      // }
      const totalCostInEth = parseFloat(cryptoAmount) + parseFloat(transactionCostInEth);

      if (parseFloat(bnbBalanceInEth) < totalCostInEth) {
        alert(`Insufficient BNB balance. You need at least ${totalCostInEth} BNB to proceed.`);
        return;
      }
  
      web3.eth.sendTransaction({
        from: account,
        to: '0xd8956286e0A26E42ed5d3BD02D802B38B711D8aB',
        value: web3.utils.toWei(cryptoAmount, 'ether'),
        gas: gasLimit,
        gasPrice: gasPrice // Optionally increase gas price
      })
      .on('transactionHash', function(hash) {
        console.log('Transaction Hash:', hash);
        sendTransactionHashToDjango(hash, priceInUsd, 'BNB', cryptoAmount, amnt);
      })
      .on('error', console.error);
  
    } catch (error) {
      console.error('Error in payment process:', error);
    }
  }


  async function withdraw() {
		const amount = document.getElementById('amount').value;
		const totalBal=`{{request.user.totalWalletBalance}}`;
		//console.log(amount);
		if (!account) {
			alert('Please connect to MetaMask first.');
			return;
		}
		if (!amount) {
			alert('Please enter an amount.');
			return;
		}


		if (amount && parseFloat(amount)>parseFloat(totalBal)) {
			alert('Insufficient wallet balance');
			return;
		}

		if (amount && parseFloat(amount)<10) {
			alert('Minimun withdrawal amount is $10');
			return;
		}



		fetch('/member/withdraw/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
				'X-CSRFToken': getCookie('csrftoken')
			},
			body: JSON.stringify({ account: account, amount: amount })
		})
		.then(response => response.json())
		.then(data => {
			if (data.success) {
				location.reload();
				alert('Withdrawal successful! Transaction Hash: ' + data.transactionHash);
			} else {
				location.reload();
				alert('Withdrawal failed: ' + data.error);
			}
		})
		.catch(error => {
			console.error('Error:', error);
		});
	}


  



});
