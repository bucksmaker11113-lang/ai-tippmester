import { useRef } from "react";
import { useFrame } from "@react-three/fiber";
import * as THREE from "three";

export default function CoreSphere() {
  const mesh = useRef();
  const glow = useRef();

  useFrame((state) => {
    const t = state.clock.getElapsedTime();

    // pulzálás
    const scale = 1 + Math.sin(t * 3) * 0.08;
    mesh.current.scale.set(scale, scale, scale);

    // lassú forgás
    mesh.current.rotation.y += 0.002;

    // glow pulzál
    glow.current.material.opacity = 0.35 + Math.sin(t * 4) * 0.15;
  });

  return (
    <group>
      {/* belső gömb */}
      <mesh ref={mesh}>
        <sphereGeometry args={[1, 64, 64]} />
        <meshStandardMaterial
          color={"#0dd4ff"}
          emissive={"#0dd4ff"}
          emissiveIntensity={1.7}
          metalness={0.2}
          roughness={0.1}
          transparent
          opacity={0.85}
        />
      </mesh>

      {/* külső fény aura */}
      <mesh ref={glow}>
        <sphereGeometry args={[1.45, 64, 64]} />
        <meshBasicMaterial
          color={"#11cfff"}
          transparent
          opacity={0.4}
          blending={THREE.AdditiveBlending}
        />
      </mesh>
    </group>
  );
}
