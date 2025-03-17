import { Web3Provider } from "./Web3Provider";
import { ConnectKitButton } from "connectkit";

const App = () => {
  return (
    <Web3Provider>
      <ConnectKitButton />
    </Web3Provider>
  );
};