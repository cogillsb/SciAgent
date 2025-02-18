# Real-Time PCR Protocol

## Materials Required
- qPCR instrument
- qPCR master mix (containing Taq polymerase, dNTPs, buffer, and fluorescent reporter)
- Forward and reverse primers (10 µM each)
- Template DNA/cDNA
- Nuclease-free water
- Optical PCR tubes/plates
- Optical adhesive film
- Micropipettes and filtered tips
- Ice bucket
- Centrifuge
- Vortex mixer

## Safety Precautions
- Wear appropriate PPE (lab coat, gloves)
- Work in a clean, designated PCR workspace
- Use separate areas for template preparation and reaction setup
- Use filtered tips to prevent cross-contamination

## Procedure

### 1. Reaction Setup
1. Thaw all reagents on ice
2. Vortex and briefly centrifuge all components before use
3. Prepare master mix for all reactions plus 10% extra volume

For each 20 µL reaction:
- 10 µL 2X qPCR master mix
- 1 µL forward primer (500 nM final)
- 1 µL reverse primer (500 nM final)
- X µL template DNA/cDNA (1-100 ng)
- Nuclease-free water to 20 µL

### 2. Sample Preparation
1. Label tubes/plates clearly
2. Dispense master mix into tubes/wells
3. Add template DNA/controls to appropriate wells
4. Seal tubes/plate with optical film
5. Centrifuge briefly (30 seconds at 1000 × g)

### 3. Instrument Setup
1. Create a new experiment in the qPCR software
2. Define sample information and plate layout
3. Select fluorophore(s)
4. Program thermal cycling conditions:

Standard Cycling Parameters:
- Initial denaturation: 95°C for 3 minutes
- 40 cycles of:
  - Denaturation: 95°C for 15 seconds
  - Annealing/Extension: 60°C for 60 seconds
- Melt curve analysis (if using SYBR Green):
  - 95°C for 15 seconds
  - 60°C for 60 seconds
  - Ramp to 95°C (0.3°C/second)

### 4. Controls
Include for each run:
- No template control (NTC)
- Positive control
- Internal control (if applicable)
- Standard curve samples (if performing absolute quantification)

### 5. Data Analysis
1. Check amplification curves for:
   - Exponential phase
   - Plateau phase
   - Background noise
2. Verify controls:
   - No amplification in NTC
   - Expected Cq values for positive controls
3. Check melt curves (SYBR Green):
   - Single peak indicates specific amplification
   - Multiple peaks suggest non-specific products
4. Calculate relative or absolute quantification as needed

## Troubleshooting

### Common Issues:
1. No amplification
   - Check reagent quality
   - Verify primer design
   - Confirm template integrity

2. Late amplification
   - Increase template amount
   - Optimize primer concentration
   - Check reagent storage conditions

3. Non-specific products
   - Optimize annealing temperature
   - Redesign primers
   - Check template quality

### Important Notes
- Keep all reagents and samples on ice during setup
- Avoid repeated freeze-thaw cycles of reagents
- Use calibrated pipettes
- Include technical replicates
- Monitor equipment calibration status

## Data Recording
Maintain detailed records of:
- Reagent lot numbers
- Template sources and concentrations
- Primer sequences
- Thermal cycling conditions
- Raw data files
- Analysis parameters
