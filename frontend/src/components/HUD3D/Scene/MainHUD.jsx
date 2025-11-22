import { Canvas } from "@react-three/fiber";
import { Suspense, useState } from "react";
import Cameras from "./Cameras.jsx";
import Lights from "./Lights.jsx";
import BloomEffect from "../Effects/BloomEffect.jsx";

// CORE 3D
import CoreSphere from "../Core/CoreSphere.jsx";
import HoloRings from "../Core/HoloRings.jsx";
import HoloGrid from "../Grid/HoloGrid.jsx";
import ScanWave from "../Grid/ScanWave.jsx";
import FloorGlow from "../Grid/FloorGlow.jsx";

// PANELS
import TipSelector from "../Panels/TipSelector.jsx";
import TipPanel3D from "../Panels/TipPanel3D.jsx";
import LiveOddsHUD from "../Panels/LiveOddsHUD.jsx";

// CHAT
import ChatPanelHUD from "../../Chat/ChatPanelHUD.jsx";

export default function MainHUD() {
  const [mode, setMode] = useState(null);

  const handleSelect = (m) => {
    setMode(m);
  };

  const closePanel = () => {
    setMode(null);
  };

  return (
    <div style={{ width: "100vw", height: "100vh", background: "#020B18" }}>
      
      {/* UI OVERLAY */}
      <TipSelector onSelect={handleSelect} />
      <LiveOddsHUD />
      <ChatPanelHUD />

      {/* POPUP PANEL */}
      <TipPanel3D mode={mode} onClose={closePanel} />

      {/* 3D WORLD */}
      <Canvas
        camera={{ position: [0, 2.5, 6], fov: 52 }}
        gl={{ antialias: true }}
      >
        <Suspense fallback={null}>
          <Cameras />
          <Lights />
          <BloomEffect />

          {/* 3D CORE */}
          <CoreSphere />
          <HoloRings />

          {/* GRID */}
          <HoloGrid />
          <ScanWave />
          <FloorGlow />
        </Suspense>
      </Canvas>
    </div>
  );
}
