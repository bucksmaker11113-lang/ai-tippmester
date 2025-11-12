import React from "react";
import { Canvas } from "@react-three/fiber";
import { Sphere, MeshDistortMaterial, OrbitControls } from "@react-three/drei";

export default function OddsSphere3D() {
  return (
    <div className="odds-sphere">
      <Canvas camera={{ position: [0, 0, 5] }}>
        <ambientLight intensity={0.8} />
        <directionalLight position={[2, 2, 2]} />
        <Sphere visible args={[1.5, 64, 64]}>
          <MeshDistortMaterial
            color="#2dfb7b"
            attach="material"
            distort={0.3}
            speed={2}
          />
        </Sphere>
        <OrbitControls enableZoom={false} />
      </Canvas>
    </div>
  );
}
