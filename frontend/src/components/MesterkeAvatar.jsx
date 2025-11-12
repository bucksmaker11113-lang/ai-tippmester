import React from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, useGLTF } from "@react-three/drei";

function MesterkeModel() {
  const { scene } = useGLTF("/assets/mesterke.glb");
  return <primitive object={scene} scale={1.5} />;
}

export default function MesterkeAvatar() {
  return (
    <div className="mesterke-avatar">
      <Canvas camera={{ position: [0, 0, 5] }}>
        <ambientLight intensity={1.2} />
        <directionalLight position={[3, 3, 3]} />
        <MesterkeModel />
        <OrbitControls enableZoom={false} />
      </Canvas>
      <div className="mesterke-text">„Ne az erő, hanem az odds legyen veled!” 😄</div>
    </div>
  );
}
