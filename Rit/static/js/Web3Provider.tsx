import { ConnectKitProvider, ConnectButton } from "@family/connectkit";
import { WagmiConfig, createClient } from "wagmi";
import { getDefaultProvider } from "ethers";

const client = createClient({
  autoConnect: true,
  provider: getDefaultProvider(),
});

function App() {
  return (
    <WagmiConfig client={client}>
      <ConnectKitProvider>
        <ConnectButton />
      </ConnectKitProvider>
    </WagmiConfig>
  );
}

export default App;
